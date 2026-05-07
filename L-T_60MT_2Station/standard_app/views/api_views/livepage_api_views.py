from django.http import JsonResponse
from standard_app.services.livepage_service import get_active_testbtn,get_size_class,get_pressure_duration,truncate_currentstatus_service,get_chart_data_service,update_pressure_analysis_service,get_result_status_service,reset_test_service,get_serialno_automode, reset_all_service
from standard_app import tasks
import json
from django.db import connection
import threading
from django.views.decorators.csrf import csrf_exempt
from standard_app.src import HmiAddress
from standard_app.views.api.single_live_page_api_views import write_to_hmi


def _hmi_write_zero_for_inactive_station_slots(size_class_rows):
    """
    For each station slot 1–4 that has no Enabled row in master_temp_data, write Sx_STATUS=0 to HMI.
    Active slots (present in size_class_rows by id) are not modified here.
    """
    if not tasks.check_hmi_connection():
        return
    active_ids = set()
    for row in size_class_rows or []:
        rid = row.get("id")
        if rid is not None:
            try:
                active_ids.add(int(rid))
            except (TypeError, ValueError):
                continue
    address_map = {
        1: HmiAddress.S1_STATUS,
        2: HmiAddress.S2_STATUS
    }
    for sid in (1, 2):
        if sid not in active_ids:
            try:
                write_to_hmi(address_map[sid], 0)
            except Exception as e:
                print(f"HMI write S{sid}_STATUS=0 (inactive / no Enabled row): {e}")


def get_active_testbtn_api(request):
    test_buttons = get_active_testbtn()
    return JsonResponse({"status":"success","test_buttons": test_buttons, "test_count": len(test_buttons)})

def get_size_class_api(request):
    size_class = get_size_class()
    _hmi_write_zero_for_inactive_station_slots(size_class)
    return JsonResponse({"status":"success","data": size_class})


def get_pressure_duration_api(request, test_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    data = json.loads(request.body)
    serial_list = data.get("serial_numbers", [])

    tasks.current_test_id = test_id
    pressure_duration = get_pressure_duration(test_id, serial_list)
        
    if pressure_duration and len(pressure_duration) > 0:
        data = pressure_duration[0]
        set_pressure = data.get('set_pressure')
        pressure_unit = data.get('pressure_unit')

        # Normalize unit (temp_testing_data.TESTING_PR_UNIT is sometimes lower-case)
        unit_norm = (pressure_unit or "").strip().upper()

        # Live system HMI registers (matches refer.py usage)
        SET_PRESSURE_ADDR = 2000
        VALVE_SIZE_ID_ADDR = 2001
        VALVE_CLASS_ID_ADDR = 2002
        SET_TIME_ADDR = 2003
        TEST_TYPE_ADDR = 2004

        # Scale pressure for BAR (HMI expects decibar)
        set_pressure_to_write = set_pressure
        if unit_norm == 'BAR' and set_pressure_to_write is not None:
            set_pressure_to_write = set_pressure_to_write * 10

        # Enable relevant stations automagically
        if tasks.check_hmi_connection():
            try:
                # Map station IDs to their HMI Status/Enable registers
                address_map = {
                    1: HmiAddress.S1_STATUS,
                    2: HmiAddress.S2_STATUS
                }
                
                with connection.cursor() as cursor:
                    # Find which station IDs correspond to the provided serial numbers
                    cursor.execute("""
                        SELECT id FROM master_temp_data 
                        WHERE id IS NOT NULL AND VALVE_SER_NO IN %s
                    """, [tuple(serial_list) if serial_list else ('',)])
                    active_ids = [row[0] for row in cursor.fetchall()]
                    
                    for sid in active_ids:
                        addr = address_map.get(sid)
                        if addr:
                            write_to_hmi(addr, 1) # Force Enable station
            except Exception as e:
                print(f"Error auto-enabling stations: {e}")

        if tasks.check_hmi_connection():
            try:
                # Look up valve size/class IDs from DB (needed for HMI writes)
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT SIZE_NAME, CLASS_NAME
                        FROM master_temp_data
                        WHERE STATION_STATUS = %s
                        LIMIT 1
                    """, ["Enabled"])
                    sc_row = cursor.fetchone()

                size_id = None
                class_id = None
                if sc_row:
                    size_name, class_name = sc_row[0], sc_row[1]
                    with connection.cursor() as cursor:
                        if size_name:
                            # Newer schema uses VALVE_SIZE_ID / VALVE_SIZE_NAME (see form_service.py + sql dump)
                            try:
                                cursor.execute("SELECT VALVE_SIZE_ID FROM valvesize WHERE VALVE_SIZE_NAME=%s", [size_name])
                                r = cursor.fetchone()
                                if r:
                                    size_id = r[0]
                            except Exception:
                                # Fallback legacy column names
                                cursor.execute("SELECT SIZE_ID FROM valvesize WHERE SIZE_NAME=%s", [size_name])
                                r = cursor.fetchone()
                                if r:
                                    size_id = r[0]
                        if class_name:
                            # Newer schema uses VALVE_CLASS_ID / VALVE_CLASS_NAME
                            try:
                                cursor.execute("SELECT VALVE_CLASS_ID FROM valveclass WHERE VALVE_CLASS_NAME=%s", [class_name])
                                r = cursor.fetchone()
                                if r:
                                    class_id = r[0]
                            except Exception:
                                # Fallback legacy column names
                                cursor.execute("SELECT CLASS_ID FROM valveclass WHERE CLASS_NAME=%s", [class_name])
                                r = cursor.fetchone()
                                if r:
                                    class_id = r[0]

                # Write required values to HMI
                if set_pressure_to_write is not None:
                    tasks.TesleadSmartsyncx.write_register(SET_PRESSURE_ADDR, int(set_pressure_to_write))
                tasks.TesleadSmartsyncx.write_register(SET_TIME_ADDR, int(data.get('set_time') or 0))
                tasks.TesleadSmartsyncx.write_register(TEST_TYPE_ADDR, int(tasks.current_test_id or 0))
                if size_id is not None:
                    tasks.TesleadSmartsyncx.write_register(VALVE_SIZE_ID_ADDR, int(size_id))
                if class_id is not None:
                    tasks.TesleadSmartsyncx.write_register(VALVE_CLASS_ID_ADDR, int(class_id))
            except Exception as e:
                print(f"HMI write failed in get_pressure_duration_api: {e}")
            
            
        else:
            print("HMI not connected")
            
        return JsonResponse({
                'status': 'success', 
                'pressure': data.get('set_pressure'), 
                'duration': data.get('set_time'),
                'class_name': data.get('class_name'),
                'duration': data.get('set_time'),
                'test_medium': data.get('test_medium')
            })
        
        
            
    else:
        return JsonResponse({'status': 'failure', 'error': 'No pressure duration found'}, status=404)
   


def get_pressure_data_api(request):
    chart_data = get_chart_data_service()
    s1_valvestatus = s2_valvestatus = s1_result_pressure = s2_result_pressure = Actual_time = None
    if chart_data:
        s1_valvestatus, s2_valvestatus, s1_result_pressure, s2_result_pressure, Actual_time = get_result_status_service()

    return JsonResponse({
            'status': 'success',
            'test_id': tasks.current_test_id,
            'timeData1': chart_data[1],
            'pressureData1': chart_data[0],
            'timerStatus1': chart_data[2],
            'timeData2': chart_data[4],
            'pressureData2': chart_data[3],
            'timerStatus2': chart_data[5],
            's1_valvestatus': s1_valvestatus,
            's2_valvestatus': s2_valvestatus,
            'S1_result_pressure': s1_result_pressure,
            'S2_result_pressure': s2_result_pressure,
            'Actual_time': Actual_time
        })

@csrf_exempt
def toggle_station_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        station_id = data.get("station_id")
        enable = data.get("enable") # 1 for enable, 0 for disable
        
        if not tasks.check_hmi_connection():
            return JsonResponse({"status": "error", "message": "HMI not connected"}, status=503)
            
        address_map = {
            1: HmiAddress.S1_STATUS,
            2: HmiAddress.S2_STATUS
        }
        
        address = address_map.get(station_id)
        if address:
            try:
                write_to_hmi(address, 1 if enable else 0)
                return JsonResponse({"status": "success", "station_id": station_id, "enabled": enable})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)}, status=500)
                
        return JsonResponse({"status": "error", "message": "Invalid station ID"}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def get_station_status_api(request):
    """Get current status of all stations from HMI"""
    if not tasks.check_hmi_connection():
        return JsonResponse({"status": "error", "message": "HMI not connected"}, status=503)
        
    try:
        s1_status = tasks.TesleadSmartsyncx.read_holding_registers(HmiAddress.S1_STATUS, 1).registers[0]
        s2_status = tasks.TesleadSmartsyncx.read_holding_registers(HmiAddress.S2_STATUS, 1).registers[0]

        return JsonResponse({
            "status": "success",
            "s1_status": s1_status,
            "s2_status": s2_status
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
def update_pressure_analysis_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        testId = data.get("testId")
        pressure_data = data.get("pressure_data")
        time_data = data.get("time_data")
        chart = data.get("chart")
        status = data.get("status")

        results_by_station, valve_ser_no = update_pressure_analysis_service(testId, pressure_data, time_data, chart, status)

        # Build response with per-station results (T1, T2)
        response = {"status": "success"}
        for station_id in [1, 2]:
            station_data = results_by_station.get(station_id, {})
            response[f"S{station_id}_result_status"] = station_data.get("result_status")
            response[f"S{station_id}_result_pressure"] = station_data.get("result_pressure")

        return JsonResponse(response)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

def start_test_thread_api(request):
    if not tasks.is_running:
        threading.Thread(target=tasks.start_pressure_collection, daemon=True).start()
        return JsonResponse({'status': 'success', 'message': 'Pressure collection started'})
    else:
        return JsonResponse({'status': 'success', 'message': 'Pressure collection already running'})


def stop_test_thread_api(request):
    try:
        response = tasks.stop_pressure_collection()
        if response is not None:
            return response
            
        # truncate_currentstatus()
        return JsonResponse({'status': 'success', 'message': 'Pressure collection stopped'})
    except Exception as e:
        return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)

def stop_pressure_collection_only_api(request):
    """Stop pressure collection without truncating tables - used for reset"""
    try:
        # Just stop the collection thread, don't truncate tables
        tasks.is_running = False
        return JsonResponse({'status': 'success', 'message': 'Pressure collection stopped for reset'})
    except Exception as e:
        return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)

def truncate_currentstatus():
   result = truncate_currentstatus_service()
   if result:
       return JsonResponse({'status': 'success', 'message': 'Current status truncated'})
   else:
       return JsonResponse({'status': 'failure', 'error': 'Failed to truncate current status'}, status=500)

@csrf_exempt
def reset_test_api(request, test_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    data = json.loads(request.body)
    valve_ser_no = data.get("valve_ser_no")
    print('valve_ser_no',valve_ser_no)
    reset_test_service(test_id, valve_ser_no)
    return JsonResponse({'status': 'success', 'message': 'Test reset successfully'})

def get_machine_mode_api(request):
    if not tasks.TesleadSmartsyncx:
        # Try to establish HMI connection first
        if not tasks.check_hmi_connection():
            return JsonResponse({'status': 'error', 'message': 'HMI not connected', 'machine_mode': 'Unknown'})
    try:
        machine_mode = tasks.TesleadSmartsyncx.read_holding_registers(HmiAddress.MACHINE_MODE,1).registers[0]
        if machine_mode == 1:
            machine_mode = "Manual"
        elif machine_mode == 0:
            machine_mode = "Auto"
        print('machine_mode',machine_mode)
        return JsonResponse({'status': 'success', 'machine_mode': machine_mode})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e), 'machine_mode': 'Unknown'})

def get_automode_response_api(request):
    if not tasks.TesleadSmartsyncx:
        return JsonResponse({'status': 'failure', 'error': 'HMI not connected'}, status=503)
    try:
        valve_ser_no = get_serialno_automode()
        cycle_start = tasks.TesleadSmartsyncx.read_holding_registers(HmiAddress.CYCLE_START_STOP,1).registers[0]
        timer_status = tasks.TesleadSmartsyncx.read_holding_registers(HmiAddress.TIMER_STATUS,1).registers[0]
        if cycle_start == 1:
            Hmi_testtype = tasks.TesleadSmartsyncx.read_holding_registers(HmiAddress.HMI_TEST_TYPE,1).registers[0]
            if Hmi_testtype > 0 and timer_status == 0:
                tasks.TesleadSmartsyncx.write_register(HmiAddress.TEST_TYPE, Hmi_testtype)
                return JsonResponse({'status': 'success', 'Test_type': Hmi_testtype,'valve_ser_no': valve_ser_no}) 
        return JsonResponse({'status': 'waiting', 'message': 'No test type found or cycle not started'})
    except Exception as e:
        return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)

def reset_all_api(request):
    cycle_status = reset_all_service()
    if cycle_status == "Cycle is running":
        return JsonResponse({'status': 'failure', 'error': 'Cycle is running'})
    return JsonResponse({'status': 'success', 'message': 'All tests reset successfully'})


