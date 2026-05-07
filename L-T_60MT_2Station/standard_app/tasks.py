import time
from django.db import connection
from django.http import JsonResponse
from pymodbus.client import ModbusTcpClient
from standard_app.src import HmiAddress
from standard_app.services.user_config_service import get_hmi_address

# HMI Connection
TesleadSmartsyncx = None
_tasks_hmi_host = None
is_running = False
current_test_id = None


def _ensure_tasks_hmi_client():
    """Build or refresh Modbus client from hmi_abrs_address.HMI_IP (same source as configuration UI)."""
    global TesleadSmartsyncx, _tasks_hmi_host
    host = get_hmi_address()
    if not host or not str(host).strip():
        print("WARNING: HMI IP not configured in database (hmi_abrs_address.HMI_IP)")
        return False
    host = str(host).strip()
    if _tasks_hmi_host != host or TesleadSmartsyncx is None:
        if TesleadSmartsyncx is not None:
            try:
                TesleadSmartsyncx.close()
            except Exception:
                pass
        TesleadSmartsyncx = ModbusTcpClient(host, timeout=1)
        _tasks_hmi_host = host
    return True


def check_hmi_connection():
    global TesleadSmartsyncx
    try:
        if not _ensure_tasks_hmi_client():
            return False
        # Connect first; then validate by reading any known-safe register.
        # This project has multiple address maps in use, so we try a small set.
        TesleadSmartsyncx.connect()

        candidate_regs = [
            getattr(HmiAddress, "S1_PRESSURE", None),
            2008,  # station 1 pressure (used in refer.py/livepage)
            2000,  # some HMIs expose pressure here
        ]

        for reg in candidate_regs:
            if not isinstance(reg, int):
                continue
            try:
                rr = TesleadSmartsyncx.read_holding_registers(reg, 1)
                if rr and hasattr(rr, "registers") and rr.registers:
                    _ = rr.registers[0]  # accept 0 as valid
                    return True
            except Exception:
                continue

        print("Error reading from HMI (no candidate register succeeded)")
    except Exception as e:
        print(e)



def perform_reading_loop():
    global is_running, current_test_id

    while is_running:
        try:
            if check_hmi_connection():

                pressure1 = TesleadSmartsyncx.read_holding_registers(HmiAddress.S1_PRESSURE, 1).registers[0]
                pressure2 = TesleadSmartsyncx.read_holding_registers(HmiAddress.S2_PRESSURE, 1).registers[0]
                pressure3 = TesleadSmartsyncx.read_holding_registers(HmiAddress.S3_PRESSURE, 1).registers[0]
                pressure4 = TesleadSmartsyncx.read_holding_registers(HmiAddress.S4_PRESSURE, 1).registers[0]
                Timer_status = TesleadSmartsyncx.read_holding_registers(HmiAddress.TIMER_STATUS, 1).registers[0]
                s1_result = TesleadSmartsyncx.read_holding_registers(HmiAddress.S1_RESULT, 1).registers[0]
                s2_result = TesleadSmartsyncx.read_holding_registers(HmiAddress.S2_RESULT, 1).registers[0]
                s3_result = TesleadSmartsyncx.read_holding_registers(HmiAddress.S3_RESULT, 1).registers[0]
                s4_result = TesleadSmartsyncx.read_holding_registers(HmiAddress.S4_RESULT, 1).registers[0]

                pressure_map = {
                    1: pressure1,
                    2: pressure2,
                    3: pressure3,
                    4: pressure4,
                }

                result_map = {
                    1: s1_result,
                    2: s2_result,
                    3: s3_result,
                    4: s4_result,
                }

                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT ID, VALVE_SER_NO,PRESSURE_UNIT
                        FROM master_temp_data 
                        WHERE STATION_STATUS='Enabled'
                    """)
                    active_stations = cursor.fetchall()

                for station_id, valve_ser_no, pressure_unit in active_stations:

                    pressure_value = pressure_map.get(station_id)
                    if pressure_unit.lower() == "bar":
                        pressure_value = pressure_value / 10

                    result_value = result_map.get(station_id)

                    if pressure_value is not None:

                        table_name = f"current_status_station{station_id}"

                        with connection.cursor() as cursor:
                            cursor.execute(f"""
                                INSERT INTO {table_name}
                                (VALVE_SERIAL_NO, STATION, PRESSURE, TEST_ID, TIMER_STATUS, RESULT)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            """, [
                                valve_ser_no,
                                station_id,
                                pressure_value,
                                current_test_id,
                                Timer_status,
                                result_value
                            ])

        except Exception as e:
            print(f"Error in loop: {e}")

        time.sleep(1)

# Start function
def start_pressure_collection():
    global is_running
    is_running = True
    perform_reading_loop()


# Stop function
def stop_pressure_collection():
    global is_running
    Pressure_drain = TesleadSmartsyncx.read_holding_registers(HmiAddress.PRESSURE_DRAIN,1).registers[0]
    if Pressure_drain == 0:
        is_running = False
        print("Stopping thread...")
    else:
        return JsonResponse({'status': 'failure', 'message': 'Pressure collection not stopped'})