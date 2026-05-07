from django.db import connection
from standard_app import tasks
from datetime import datetime, date
from standard_app.src import HmiAddress

def get_active_testbtn():
    with connection.cursor() as cursor:
        # Custom test order:
        # 1 -> 29 -> 2 -> 3 -> 49 -> 4 -> 5 -> 6 ...
        # IMPORTANT: use only the "common" test rows (VALVE_SERIAL_NO IS NULL)
        # and de-duplicate by TEST_ID to avoid button repeats like 1 -> 29 -> 1 -> 2 ...
        cursor.execute("""
            SELECT TEST_ID, MIN(TEST_NAME) AS TEST_NAME
            FROM temp_testing_data
            WHERE VALVE_SERIAL_NO IS NULL
            GROUP BY TEST_ID
            ORDER BY
              CASE
                WHEN TEST_ID = 29 THEN 110
                WHEN TEST_ID = 49 THEN 310
                ELSE TEST_ID * 100
              END ASC
        """)
        results = cursor.fetchall()

        cursor.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS='Enabled'")
        valve_ser_no = cursor.fetchall()
        valve_ser_no = [row[0] for row in valve_ser_no]
        
        if results:
            return [{'test_id': row[0], 'test_btn': row[1], 'valve_ser_no': valve_ser_no} for row in results]
        else:
            return []  # Return empty list if no active buttons found

def get_size_class():
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID,VALVE_SER_NO,PRESSURE_UNIT,SIZE_NAME,CLASS_NAME,TYPE_NAME,SHELL_MATERIAL_NAME,COL8_VALUE FROM master_temp_data where STATION_STATUS='Enabled'")
        results = cursor.fetchall()
        if results:
            return [{'id': row[0],'valve_ser_no': row[1], 'pressure_unit': row[2], 'size_name': row[3], 'class_name': row[4], 'type_name': row[5], 'shell_material_name': row[6], 'tested_by': row[7]} for row in results]
        else:
            return []  # Return empty list if no active buttons found
       

def get_pressure_duration(test_id,valve_ser_no):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT PRESSURE_UNIT,CLASS_NAME FROM master_temp_data WHERE STATION_STATUS = %s",['Enabled']
        )
        row = cursor.fetchone()

        if not row:
            return []

        pressure_unit = row[0]
        class_name = row[1]
        column_map = {
            "BAR": "TESTING_PR_BAR",
            "PSI": "TESTING_PR_PSI",
            "KG/CM2G": "TESTING_PR_KGCM2"
        }

        # Handle case-insensitivity or extra spaces
        if pressure_unit:
            pressure_unit = pressure_unit.strip().upper()

        column = column_map.get(pressure_unit)
        if not column:
            return []

        query = f"""
            SELECT {column}, TESTING_DUR_SEC,TEST_NAME,TEST_MEDIUM,TESTING_PR_UNIT
            FROM temp_testing_data
            WHERE TEST_ID = %s
        """

        cursor.execute(query, [test_id])
        results = cursor.fetchall()
        insert_pressureanalysis(test_id,results,valve_ser_no)
        return [
            {"set_pressure": r[0], "set_time": r[1], "class_name": class_name, "test_medium": r[3], "pressure_unit": r[4]}
            for r in results
        ]

def insert_pressureanalysis(test_id, results, valve_ser_no):

    if not results:
        return
    

    set_pressure = results[0][0]
    set_time = results[0][1]
    test_name = results[0][2]

    tables = ['temp_pressure_analysis']

    with connection.cursor() as cursor:
        # Get active station data
        # Dynamically build the column list for COL1 to COL65
        col_list = []
        for i in range(1, 66):
            col_list.append(f"COL{i}_NAME")
            col_list.append(f"COL{i}_VALUE")
        col_str = ", ".join(col_list)

        cursor.execute(f"""
            SELECT VALVE_SER_NO, PRESSURE_UNIT, STANDARD_NAME,
                   SIZE_NAME, CLASS_NAME, TYPE_NAME, SHELL_MATERIAL_NAME,
                   DURATION_TYPE,
                   {col_str}
            FROM master_temp_data
            WHERE STATION_STATUS = 'Enabled'
        """)

        result = cursor.fetchone()
        if not result:
            return

        for valve_ser_nos in valve_ser_no:

            cursor.execute("SELECT Count_No FROM serial_tbl WHERE Serial_No = %s",[valve_ser_nos])
            count_no = cursor.fetchone()
            if count_no:
                count_no = count_no[0] + 1
            else:
                count_no = 1

            #  Loop for both tables
            for table in tables:

                # Check existence
                cursor.execute(
                    f"SELECT 1 FROM {table} WHERE VALVE_SER_NO = %s and TEST_ID = %s and COUNT_ID = %s",
                    [valve_ser_nos,test_id,count_no]
                )

                exists = cursor.fetchone()

                if exists:
                    # UPDATE
                    # Build update set clause for dynamic columns
                    update_cols = [
                        "TEST_ID = %s", "TEST_NAME = %s", "SET_PRESSURE = %s", "SET_TIME = %s",
                        "PRESSURE_UNIT = %s", "STANDARD_NAME = %s", "VALVESIZE_NAME = %s",
                        "VALVECLASS_NAME = %s", "VALVETYPE_NAME = %s", "SHELLMATERIAL_NAME = %s",
                        "DURATION_TYPE = %s"
                    ]
                    for i in range(1, 66):
                        update_cols.append(f"COL{i}_NAME = %s")
                        update_cols.append(f"COL{i}_VALUE = %s")
                    
                    update_data = [
                        test_id, test_name, set_pressure, set_time,
                        result[1], result[2], result[3], result[4], result[5], result[6], result[7]
                    ]
                    # Add all COL data (result[8] to end)
                    update_data.extend(result[8:])
                    # Add WHERE clause values
                    update_data.extend([valve_ser_nos, test_id, count_no])

                    sql = f"UPDATE {table} SET {', '.join(update_cols)} WHERE VALVE_SER_NO = %s AND TEST_ID = %s AND COUNT_ID = %s"
                    cursor.execute(sql, update_data)

                else:
                    # INSERT
                    insert_cols = [
                        "TEST_ID", "TEST_NAME", "SET_PRESSURE", "SET_TIME",
                        "VALVE_SER_NO", "PRESSURE_UNIT", "STANDARD_NAME",
                        "VALVESIZE_NAME", "VALVECLASS_NAME",
                        "VALVETYPE_NAME", "SHELLMATERIAL_NAME", "DURATION_TYPE"
                    ]
                    for i in range(1, 66):
                        insert_cols.append(f"COL{i}_NAME")
                        insert_cols.append(f"COL{i}_VALUE")
                    insert_cols.append("COUNT_ID")

                    placeholders = ["%s"] * len(insert_cols)
                    
                    insert_data = [
                        test_id, test_name, set_pressure, set_time,
                        valve_ser_nos, result[1], result[2], result[3], result[4], result[5], result[6], result[7]
                    ]
                    insert_data.extend(result[8:])
                    insert_data.append(count_no)

                    sql = f"INSERT INTO {table} ({', '.join(insert_cols)}) VALUES ({', '.join(placeholders)})"
                    cursor.execute(sql, insert_data)

            connection.commit()

            connection.commit()


def update_pressure_analysis_service(testId, pressure_data, time_data, chart, status):
    """
    Update pressure_analysis table for the specific station (chart number).
    
    'chart' corresponds to the station ID (1=S1, 2=S2, 3=S3).
    Each call updates ONLY that station's row with the correct pressure_data.
    
    For 'on' status: sets START_PRESSURE and START time.
    For 'off' status: reads that station's HMI result register, updates RESULT_PRESSURE, 
                       END time, ACTUAL_PRESSURE, and VALVE_STATUS.
    
    Returns (results_by_station dict, valve_ser_no_list).
    """

    time_obj = datetime.strptime(time_data, "%H:%M:%S").time()
    current_time = datetime.combine(date.today(), time_obj)

    results_by_station = {}

    with connection.cursor() as cursor:
        # Get all active stations and their serial numbers
        cursor.execute("""
            SELECT ID, VALVE_SER_NO 
            FROM master_temp_data 
            WHERE STATION_STATUS = 'Enabled'
        """)
        active_stations = cursor.fetchall()  # [(id, valve_ser_no), ...]

        # Collect all active valve serial numbers
        valve_ser_no_list = [row[1] for row in active_stations]

        if not active_stations:
            return results_by_station, valve_ser_no_list

        # Find the valve_ser_no for the specific station (chart number)
        station_valve_ser_no = None
        for station_id, vsn in active_stations:
            if station_id == chart:
                station_valve_ser_no = vsn
                break

        if station_valve_ser_no is None:
            # Station not active, nothing to update
            return results_by_station, valve_ser_no_list

        cursor.execute("SELECT COUNT_ID FROM temp_pressure_analysis WHERE TEST_ID = %s AND VALVE_SER_NO = %s ORDER BY COUNT_ID DESC LIMIT 1", [testId, station_valve_ser_no])
        row = cursor.fetchone()
        count_no = row[0] if row else None

        if status == 'on':
            # Update START_PRESSURE and START for this specific station only
            cursor.execute("""
                UPDATE temp_pressure_analysis
                SET START_PRESSURE = %s,
                    START = %s
                WHERE TEST_ID = %s AND VALVE_SER_NO = %s AND COUNT_ID = %s
            """, [pressure_data, current_time, testId, station_valve_ser_no, count_no])
            connection.commit()
            return results_by_station, valve_ser_no_list

        if status == 'off':
            # Read HMI result register for this specific station
            result_value = None
            try:
                # IMPORTANT:
                # Result code registers are station-specific and DO NOT follow (2009 + chart).
                # (2009 + chart) points to timer status (ex: 2010 for station 1), which caused PASS/FAIL
                # to be derived from timer status instead of the real result register.
                result_reg_map = {
                    1: HmiAddress.S1_RESULT,
                    2: HmiAddress.S2_RESULT
                }
                result_reg = result_reg_map.get(int(chart))
                if result_reg is None:
                    raise ValueError(f"Unsupported station/chart: {chart}")
                reg = tasks.TesleadSmartsyncx.read_holding_registers(result_reg, 1)
                result_value = reg.registers[0]
            except Exception as e:
                print(f"Could not read HMI register for station {chart}: {e}")

            if result_value is not None:
                # Result decoding:
                # 2 = RUNNING, 1 = PASS, 0 = FAIL
                rv = int(result_value)
                if rv == 2:
                    result_status = 'RUNNING'
                elif rv == 1:
                    result_status = 'PASS'
                elif rv == 0:
                    result_status = 'FAIL'

                cursor.execute("""
                    UPDATE temp_pressure_analysis
                    SET RESULT_PRESSURE = %s,
                        END = %s,
                        ACTUAL_PRESSURE = %s,
                        VALVE_STATUS = CASE 
                            WHEN VALVE_STATUS IS NULL THEN %s 
                            ELSE VALVE_STATUS 
                        END,
                        CYCLE_COMPLETE = %s
                    WHERE TEST_ID = %s 
                    AND VALVE_SER_NO = %s AND COUNT_ID = %s
                """, [
                    pressure_data,
                    current_time,
                    pressure_data,
                    result_status,
                    'No',
                    testId,
                    station_valve_ser_no, 
                    count_no  
                ])

                results_by_station[chart] = {
                    'result_status': result_status,
                    'result_pressure': pressure_data
                }

            connection.commit()

    return results_by_station, valve_ser_no_list

def get_result_status_service():
    """
    Get VALVE_STATUS and RESULT_PRESSURE for each active station (1–2) plus HMI actual time.
    Returns (s1_status, s2_status, s1_pressure, s2_pressure, Actual_time).
    """
    if not tasks.current_test_id:
        return None, None, None, None, None

    station_statuses = {1: None, 2: None}
    station_pressures = {1: None, 2: None}
    Actual_time = None

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, VALVE_SER_NO 
            FROM master_temp_data 
            WHERE STATION_STATUS = 'Enabled'
        """)
        active_stations = cursor.fetchall()

        if not active_stations:
            return None, None, None

        for station_id, valve_ser_no in active_stations:
            if station_id not in station_statuses:
                continue
            
            # Retrieve valve status and result pressure from temp_pressure_analysis table instead of HMI
            cursor.execute("""
                SELECT VALVE_STATUS, RESULT_PRESSURE FROM temp_pressure_analysis
                WHERE TEST_ID = %s AND VALVE_SER_NO = %s
                ORDER BY COUNT_ID DESC LIMIT 1
            """, [tasks.current_test_id, valve_ser_no])
            r = cursor.fetchone()
            if r:
                station_statuses[station_id] = r[0]
                station_pressures[station_id] = r[1]
            else:
                station_statuses[station_id] = "RUNNING"
                station_pressures[station_id] = None

        try:
            if tasks.TesleadSmartsyncx:
                response = tasks.TesleadSmartsyncx.read_holding_registers(HmiAddress.ACTUAL_TIME, 1)
                if not response.isError():
                    Actual_time = response.registers[0]
        except Exception as e:
            print(f"Error reading ACTUAL_TIME: {e}")
            Actual_time = None

    return (
        station_statuses[1],
        station_statuses[2],
        station_pressures[1],
        station_pressures[2],
        Actual_time,
    )

def start_test1():
    with connection.cursor() as cursor:
        if tasks.current_test_id:
            cursor.execute("SELECT PRESSURE, DATE_FORMAT(DATE_TIME, '%%l:%%i:%%s') AS formatted_time, TIMER_STATUS FROM current_status_station1 WHERE TEST_ID = %s ORDER BY DATE_TIME ASC", [tasks.current_test_id])
        else:
            cursor.execute("SELECT PRESSURE, DATE_FORMAT(DATE_TIME, '%%l:%%i:%%s') AS formatted_time, TIMER_STATUS FROM current_status_station1 ORDER BY DATE_TIME ASC")
        pressure1 = cursor.fetchall()
        
        if pressure1:
            pressures = [row[0] for row in pressure1]
            durations = [row[1] for row in pressure1] # Depending on format, frontend might need conversion
            timer_status = [row[2] for row in pressure1]
            return pressures, durations, timer_status
        else:
            print("No results found in start_test1")
            return [], [], []

def start_test2():
    with connection.cursor() as cursor:
        if tasks.current_test_id:
            cursor.execute("SELECT PRESSURE, DATE_FORMAT(DATE_TIME, '%%l:%%i:%%s') AS formatted_time, TIMER_STATUS FROM current_status_station2 WHERE TEST_ID = %s ORDER BY DATE_TIME ASC", [tasks.current_test_id])
        else:
            cursor.execute("SELECT PRESSURE, DATE_FORMAT(DATE_TIME, '%%l:%%i:%%s') AS formatted_time, TIMER_STATUS FROM current_status_station2 ORDER BY DATE_TIME ASC")
        pressure2 = cursor.fetchall()
        
        if pressure2:
            pressures = [row[0] for row in pressure2]
            durations = [row[1] for row in pressure2] # Depending on format, frontend might need conversion
            timer_status = [row[2] for row in pressure2]
            return pressures, durations, timer_status
        else:
            print("No results found in start_test2")
            return [], [], []

def get_chart_data_service():
    pressure1, duration1, timer_status1 = start_test1()
    if not pressure1:
        pressure1 = []
        duration1 = []
        timer_status1 = []

    pressure2, duration2, timer_status2 = start_test2()
    if not pressure2:
        pressure2 = []
        duration2 = []
        timer_status2 = []

    return (
        pressure1,
        duration1,
        timer_status1,
        pressure2,
        duration2,
        timer_status2
    )


def get_pressure_data():

    table_map = {
        1: 'current_status_station1',
        2: 'current_status_station2'
    }

    final_results = {}

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT ID 
            FROM master_temp_data 
            WHERE STATION_STATUS = 'Enabled'
        """)
        active_ids = [row[0] for row in cursor.fetchall()]

        for station_id in active_ids:
            table_name = table_map.get(station_id)

            if not table_name:
                continue

            cursor.execute(f"""
                SELECT PRESSURE, DATE_TIME
                FROM {table_name}
                ORDER BY DATE_TIME DESC
                LIMIT 1
            """)

            row = cursor.fetchone()

            if row:
                final_results[f"s{station_id}"] = {
                    "pressure": float(row[0]),
                    "time": row[1].strftime('%I:%M:%S %p') if row[1] else None
                }
            else:
                final_results[f"s{station_id}"] = {
                    "pressure": 0,
                    "time": None
                }

    return final_results 

def truncate_currentstatus_service():
    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE current_status_station1")
        cursor.execute("TRUNCATE TABLE current_status_station2")
        cursor.execute("TRUNCATE TABLE temp_testing_data")
        
    connection.commit()
    return True


def reset_test_service(test_id,valve_ser_no):
    placeholders = ','.join(['%s'] * len(valve_ser_no))
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM current_status_station1 WHERE TEST_ID = %s", [test_id])
        cursor.execute("DELETE FROM current_status_station2 WHERE TEST_ID = %s", [test_id])
        cursor.execute("SELECT COUNT_ID FROM temp_pressure_analysis WHERE TEST_ID = %s", [test_id])
        count_id = cursor.fetchone()
        query = f"""
        UPDATE temp_pressure_analysis
        SET ACTUAL_PRESSURE = NULL,
            START_PRESSURE = NULL,
            RESULT_PRESSURE = NULL,
            START = NULL,
            END = NULL,
            VALVE_STATUS = NULL,
            CYCLE_COMPLETE = NULL
        WHERE TEST_ID = %s
        AND VALVE_SER_NO IN ({placeholders}) AND COUNT_ID = %s
        """
        cursor.execute(query, [test_id] + valve_ser_no + [count_id])

    connection.commit()

def get_serialno_automode():
    with connection.cursor() as cursor:
        cursor.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS='Enabled'")
        valve_ser_no = cursor.fetchall()
        valve_ser_no = [row[0] for row in valve_ser_no]
    return valve_ser_no

def reset_all_service():
    cycle_start = tasks.TesleadSmartsyncx.read_holding_registers(HmiAddress.CYCLE_START_STOP,1).registers[0]
    if cycle_start == 0:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT_ID,TEST_ID FROM temp_pressure_analysis")
            result = cursor.fetchall()
            if result:
                for count_id, test_id in result:
                    cursor.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS='Enabled'")
                    valve_ser_no = cursor.fetchall()
                    valve_ser_no = [row[0] for row in valve_ser_no]
                    placeholders = ','.join(['%s'] * len(valve_ser_no))
                    cursor.execute("TRUNCATE TABLE current_status_station1")
                    cursor.execute("TRUNCATE TABLE current_status_station2")
                    cursor.execute(
                        f"DELETE FROM pressure_analysis WHERE VALVE_SER_NO IN ({placeholders}) AND TEST_ID = %s AND COUNT_ID = %s",
                        valve_ser_no + [test_id, count_id]
                    )
                    cursor.execute("TRUNCATE TABLE temp_pressure_analysis")
            else:
                # If temp_pressure_analysis is empty, just truncate the current_status tables
                cursor.execute("TRUNCATE TABLE current_status_station1")
                cursor.execute("TRUNCATE TABLE current_status_station2")
                cursor.execute("TRUNCATE TABLE temp_pressure_analysis")

            tasks.TesleadSmartsyncx.write_register(HmiAddress.HMI_TEST_TYPE, 0)
        connection.commit()
        
        # Clear the current test ID
        tasks.current_test_id = None
    else:
        return "Cycle is running"