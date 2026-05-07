from django.db import connection, transaction
from datetime import datetime

def _to_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default

def check_hmi_connection():
    """
    Check if HMI is connected by querying configuration_table
    Returns: bool (True if connected, False otherwise)
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT HMI_CONNECTION FROM configuration_table WHERE id=1")
            result = cursor.fetchone()
            hmi_status = result[0] if result else 'Disabled'
            return hmi_status == 'Enabled'
    except Exception as e:
        print(f"Error checking HMI connection: {e}")
        return False

def check_duplicate_serial_across_stations(serial_number, current_station_id):
    """
    Check if serial number exists in any other active station
    Args:
        serial_number: The serial number to check
        current_station_id: The current station ID (1, 2)
    Returns: tuple (is_duplicate: bool, duplicate_station_id: int or None)
    """
    if not serial_number:
        return False, None
    
    serial_number = str(serial_number).strip()
    
    with connection.cursor() as cursor:
        # Check all other active stations
        cursor.execute("""
            SELECT ID, VALVE_SER_NO 
            FROM master_temp_data 
            WHERE ID != %s 
            AND STATION_STATUS = 'Enabled'
            AND VALVE_SER_NO IS NOT NULL
            AND VALVE_SER_NO != ''
        """, [current_station_id])
        
        results = cursor.fetchall()
        
        for row in results:
            station_id = row[0]
            other_serial = str(row[1]).strip() if row[1] else None
            
            if other_serial and serial_number == other_serial:
                return True, station_id
        
        return False, None

def check_duplicate_serial_station1(station1_serial):
    """
    Check if station 1 serial number matches any other active station
    Returns: tuple (is_duplicate: bool, duplicate_station_id: int or None)
    """
    return check_duplicate_serial_across_stations(station1_serial, 1)

def check_duplicate_serial_station2(station2_serial):
    """
    Check if station 2 serial number matches any other active station
    Returns: tuple (is_duplicate: bool, duplicate_station_id: int or None)
    """
    return check_duplicate_serial_across_stations(station2_serial, 2)


def save_station(query, update_values, station_id):
    try:
        with connection.cursor() as cursor:
            # 1. Update master table
            cursor.execute(query, update_values)
            if cursor.rowcount == 0:
                # Ensure a station row exists before applying the update payload.
                cursor.execute(
                    "INSERT INTO master_temp_data (ID) VALUES (%s)",
                    [station_id]
                )
                cursor.execute(query, update_values)
            connection.commit()

            # 2. Get Gauge Details for Station 1
            cursor.execute(
                """SELECT GD_SERIAL_NUMBER, GD_PRESSURE_RANGE_PSI, GD_MEDIUM,
                          GD_PRESSURE_RANGE_BAR, `GD_PRESSURE_RANGE_KG/CM2`,
                          GD_DONE_DATE, GD_DUE_DATE
                   FROM gauge_details
                   WHERE GD_STATUS=%s AND GD_STATION_ID=%s""",
                [1, station_id]
            )
            gauge_values = cursor.fetchall()
       
            # 3. Get Serial and Unit from master_temp_data
            cursor.execute("SELECT VALVE_SER_NO, PRESSURE_UNIT FROM master_temp_data WHERE ID = %s", [station_id])
            master_result = cursor.fetchone()
            station_serial = str(master_result[0]).strip() if master_result and master_result[0] else None
            pressure_unit = master_result[1] if master_result else None
            
            if station_serial:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 4. Insert into instrument test log (Station-wide instruments)
                cursor.execute(
                    """ SELECT 
                        INSTRUMENT_SERIAL_NUMBER, 
                        INSTRUMENT_TYPE, 
                        INSTRUMENT_DONE_DATE, 
                        INSTRUMENT_DUE_DATE
                    FROM instrument_categories 
                    WHERE INSTRUMENT_STATUS = 'ENABLE'""")
                instrument_values = cursor.fetchall()
        
                for inst in instrument_values:
                    cursor.execute(
                        """INSERT INTO instrument_test_log
                           (VALVE_SERIAL_NUMBER, INSTRUMENT_SERIAL_NUMBER, INSTRUMENT_TYPE,
                            INSTRUMENT_DONE_DATE, INSTRUMENT_DUE_DATE, CREATED_DATE)
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        [
                            station_serial, inst[0], inst[1],
                            inst[2], inst[3], now
                        ]
                    )

                for val in gauge_values:
                    # 4. Insert into gauge details test log
                    cursor.execute(
                        """INSERT INTO gauge_details_test_log
                           (VALVE_SERIAL_NUMBER, PRESSURE_UNIT, GD_SERIAL_NUMBER,
                            GD_STATION_ID, GD_PRESSURE_RANGE_PSI, GD_MEDIUM,
                            GD_PRESSURE_RANGE_BAR, GD_PRESSURE_RANGE_KG_CM2, 
                            GD_DONE_DATE, GD_DUE_DATE, CREATED_DATE)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        [
                            station_serial, pressure_unit, val[0],
                            "1", val[1], val[2],
                            val[3], val[4], val[5],
                            val[6], now
                        ]
                    )

                    # 5. Insert into pressure gauge analysis
                    cursor.execute(
                        """INSERT INTO pressure_gauge_analysis
                           (VALVE_SER_NO, INSTRUMENT_SER_NO, `RANGE`,
                            INSTRUMENT_TYPE, CAL_DUE_DATE, CAL_DONE_DATE, STATION_ID)
                           VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                        [
                            station_serial,
                            val[0],  # GD_SERIAL_NUMBER
                            val[1],  # GD_PRESSURE_RANGE_PSI
                            val[2],  # GD_MEDIUM
                            val[6],  # GD_DUE_DATE
                            val[5],  # GD_DONE_DATE
                            station_id
                        ]
                    )
                connection.commit()

            return True

    except Exception as e:
        print(f"Error in save_station1: {str(e)}")
        return False


def insert_pressure_duration(testname, test_pressure, test_duration, active_testid, diabled_testid, pressureunit, valve_serial_no=None, station_number=1):
    try:        
        # STEP 1: flatten active list
        active = [item[0] for item in active_testid]

        # STEP 2: convert disabled list to int
        disabled = [int(x) for x in diabled_testid if str(x).isdigit()]

        # STEP 3: Find remaining active IDs
        remaining = [tid for tid in active if tid not in disabled]
    except Exception as e:
        print(f"ERROR in insert_pressure_duration: {str(e)}")
        raise
    
    if disabled:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM temp_testing_data 
                WHERE TEST_ID IN %s AND STATION_ID = %s AND VALVE_SERIAL_NO = %s
                """,
                [tuple(disabled), station_number, valve_serial_no]
            )

    # --- FILTER matched values by remaining list ---
    filtered_testname = []
    filtered_duration = []
    filtered_pressure = []

    for i, tid in enumerate(active):
        if tid not in disabled:
            filtered_testname.append(testname[i])
            filtered_duration.append(test_duration[i])
            filtered_pressure.append(test_pressure[i])

    # Now loop through filtered values
    for i in range(len(remaining)):
        tid = remaining[i]
        tn = filtered_testname[i]
        td = filtered_duration[i]
        tp = _to_float(filtered_pressure[i])
        td = _to_float(filtered_duration[i])

        # pressure conversion
        if pressureunit.lower() == "psi":
            testing_pressure_psi = tp
            testing_pressure_bar = tp / 14.5
        else:
            testing_pressure_bar = tp
            testing_pressure_psi = tp * 14.5

        testing_duration_unit = "Sec"
        testing_duration_minutes = td / 60
        testing_pressure_kgcm2 = testing_pressure_bar

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.TEST_CATEGORY_MEDIUM, tt.TEST_CATEGORY_ID, c.PRESSURE_COLUMN_NAME, c.DURATION_COLUMN_NAME
                FROM test_type tt
                JOIN category c ON tt.TEST_CATEGORY_ID = c.TEST_CATEGORY_ID
                WHERE tt.TEST_TYPE_ID = %s
            """, [tid])
            rows = cursor.fetchall()
            if not rows:
                continue

            for row in rows:

                # -----------------------------
                # CHECK IF TEST_ID EXISTS FOR THIS STATION AND VALVE_SERIAL_NO
                # -----------------------------
                cursor.execute(
                    "SELECT COUNT(*) FROM temp_testing_data WHERE TEST_ID = %s AND STATION_ID = %s AND VALVE_SERIAL_NO = %s",
                    [tid, station_number, valve_serial_no]
                )
                exists = cursor.fetchone()[0]

                if exists:
                    # UPDATE EXISTING ROW FOR THIS STATION
                    cursor.execute("""
                        UPDATE temp_testing_data SET
                            TEST_NAME = %s,
                            TEST_MEDIUM = %s,
                            TEST_CATEGORY = %s,
                            COL_PRE = %s,
                            COL_DUR = %s,
                            TESTING_PR_UNIT = %s,
                            TESTING_PR_BAR = %s,
                            TESTING_PR_PSI = %s,
                            TESTING_PR_KGCM2 = %s,
                            TESTING_DUR_UNIT = %s,
                            TESTING_DUR_SEC = %s,
                            TESTING_DUR_MIN = %s
                        WHERE TEST_ID = %s AND STATION_ID = %s AND VALVE_SERIAL_NO = %s
                    """, [
                        tn, row[0], row[1], row[2], row[3],
                        pressureunit,
                        testing_pressure_bar, testing_pressure_psi, testing_pressure_kgcm2,
                        testing_duration_unit, td, testing_duration_minutes,
                        tid, station_number, valve_serial_no
                    ])
                else:
                    # INSERT NEW ROW FOR THIS STATION ONLY
                    cursor.execute("""
                        INSERT INTO temp_testing_data 
                        (STATION_ID,VALVE_SERIAL_NO,TEST_ID,TEST_NAME,TEST_MEDIUM,TEST_CATEGORY,COL_PRE,COL_DUR,
                        TESTING_PR_UNIT,TESTING_PR_BAR,TESTING_PR_PSI,TESTING_PR_KGCM2,
                        TESTING_DUR_UNIT,TESTING_DUR_SEC,TESTING_DUR_MIN)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, [
                        station_number, valve_serial_no, tid, tn, row[0], row[1], row[2], row[3],
                        pressureunit,
                        testing_pressure_bar, testing_pressure_psi, testing_pressure_kgcm2,
                        testing_duration_unit, td, testing_duration_minutes
                    ])
                

def insert_pressure_duration_s2(testname, test_pressure, test_duration, active_testid, diabled_testid, pressureunit, valve_serial_no_s2=None):
    try:        
        # STEP 1: flatten active list
        active = [item[0] for item in active_testid]

        # STEP 2: convert disabled list to int
        disabled = [int(x) for x in diabled_testid if str(x).isdigit()]

        # STEP 3: Find remaining active IDs
        remaining = [tid for tid in active if tid not in disabled]
    except Exception as e:
        print(f"ERROR in insert_pressure_duration_s2: {str(e)}")
        raise
    
    if disabled:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM temp_testing_data_s2 
                WHERE test_id IN %s
                """,
                [tuple(disabled)]
            )

    # --- FILTER matched values by remaining list ---
    filtered_testname = []
    filtered_duration = []
    filtered_pressure = []

    for i, tid in enumerate(active):
        if tid not in disabled:
            filtered_testname.append(testname[i])
            filtered_duration.append(test_duration[i])
            filtered_pressure.append(test_pressure[i])

    # Now loop through filtered values
    for i in range(len(remaining)):
        tid = remaining[i]
        tn = filtered_testname[i]
        td = _to_float(filtered_duration[i])
        tp = _to_float(filtered_pressure[i])

        # pressure conversion
        if pressureunit.lower() == "psi":
            testing_pressure_psi = tp
            testing_pressure_bar = tp / 14.5
        else:
            testing_pressure_bar = tp
            testing_pressure_psi = tp * 14.5

        testing_duration_unit = "Sec"
        testing_duration_minutes = td / 60
        testing_pressure_kgcm2 = testing_pressure_bar

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.TEST_CATEGORY_MEDIUM, tt.TEST_CATEGORY_ID, c.PRESSURE_COLUMN_NAME, c.DURATION_COLUMN_NAME
                FROM test_type tt
                JOIN category c ON tt.TEST_CATEGORY_ID = c.TEST_CATEGORY_ID
                WHERE tt.TEST_TYPE_ID = %s
            """, [tid])
            rows = cursor.fetchall()
            if not rows:
                continue

            for row in rows:

                # -----------------------------
                # CHECK IF TEST_ID EXISTS
                # -----------------------------
                cursor.execute(
                    "SELECT COUNT(*) FROM temp_testing_data_s2 WHERE TEST_ID = %s",
                    [tid]
                )
                exists = cursor.fetchone()[0]

                if exists:
                    # -----------------------------
                    # UPDATE EXISTING ROW
                    # -----------------------------
                    cursor.execute("""
                        UPDATE temp_testing_data_s2 SET
                            TEST_NAME = %s,
                            TEST_MEDIUM = %s,
                            TEST_CATEGORY = %s,
                            COL_PRE = %s,
                            COL_DUR = %s,
                            TESTING_PR_UNIT = %s,
                            TESTING_PR_BAR = %s,
                            TESTING_PR_PSI = %s,
                            TESTING_PR_KGCM2 = %s,
                            TESTING_DUR_UNIT = %s,
                            TESTING_DUR_SEC = %s,
                            TESTING_DUR_MIN = %s,
                            VALVE_SERIAL_NO = %s
                        WHERE TEST_ID = %s
                    """, [
                        tn, row[0], row[1], row[2], row[3],
                        pressureunit,
                        testing_pressure_bar, testing_pressure_psi, testing_pressure_kgcm2,
                        testing_duration_unit, td, testing_duration_minutes,
                        valve_serial_no_s2,
                        tid
                    ])
                else:
                    # -----------------------------
                    # INSERT NEW ROW
                    # -----------------------------
                    cursor.execute("""
                        INSERT INTO temp_testing_data_s2 
                        (TEST_ID,TEST_NAME,TEST_MEDIUM,TEST_CATEGORY,COL_PRE,COL_DUR,
                        TESTING_PR_UNIT,TESTING_PR_BAR,TESTING_PR_PSI,TESTING_PR_KGCM2,
                        TESTING_DUR_UNIT,TESTING_DUR_SEC,TESTING_DUR_MIN,VALVE_SERIAL_NO)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, [
                        tid, tn, row[0], row[1], row[2], row[3],
                        pressureunit,
                        testing_pressure_bar, testing_pressure_psi, testing_pressure_kgcm2,
                        testing_duration_unit, td, testing_duration_minutes, valve_serial_no_s2
                    ])
                    
        
       
 


def save_common_test_data(testname, test_pressure, test_duration, active_testid, disabled_testid, pressureunit):
    """
    Save test data for all active stations without serial number.
    This stores one set of values common to all active stations.
    VALVE_SERIAL_NO will be NULL to indicate this is common test data.
    """
    try:        
        # STEP 1: flatten active list - handle both list and list of tuples
        if active_testid and isinstance(active_testid[0], (list, tuple)):
            active = [item[0] for item in active_testid]
        else:
            active = active_testid  # Already a flat list

        # STEP 2: convert disabled list to int
        disabled = [int(x) for x in disabled_testid if str(x).isdigit()]

        # STEP 3: Find remaining active IDs
        remaining = [tid for tid in active if tid not in disabled]
    except Exception as e:
        print(f"ERROR in save_common_test_data: {str(e)}")
        raise

    # Remove stale common rows so livepage shows ONLY current tests.
    # Otherwise, older SAP names like "Seat ( Hydro )" can remain alongside new names.
    try:
        remaining_int = [int(x) for x in remaining if str(x).isdigit()]
        with connection.cursor() as cursor:
            if remaining_int:
                placeholders = ','.join(['%s'] * len(remaining_int))
                cursor.execute(
                    f"DELETE FROM temp_testing_data WHERE VALVE_SERIAL_NO IS NULL AND TEST_ID NOT IN ({placeholders})",
                    remaining_int
                )
            else:
                cursor.execute("DELETE FROM temp_testing_data WHERE VALVE_SERIAL_NO IS NULL")
        connection.commit()
    except Exception as e:
        print(f"WARNING: could not clear stale common tests: {e}")
    
    # Delete disabled tests from common test data table (where VALVE_SERIAL_NO IS NULL)
    if disabled:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM temp_testing_data 
                WHERE TEST_ID IN %s AND VALVE_SERIAL_NO IS NULL
                """,
                [tuple(disabled)]
            )

    # Filter matched values by remaining list
    filtered_testname = []
    filtered_duration = []
    filtered_pressure = []

    for i, tid in enumerate(active):
        if tid not in disabled:
            filtered_testname.append(testname[i])
            filtered_duration.append(test_duration[i])
            filtered_pressure.append(test_pressure[i])

    # Loop through filtered values and save
    for i in range(len(remaining)):
        tid = remaining[i]
        tn = filtered_testname[i]
        # Force DB test names (SAP names may differ)
        try:
            tid_int = int(tid)
        except Exception:
            tid_int = None
        # DB naming rules (as requested):
        # - testId 1: keep actual name from SAP/payload
        # - testId 2: force "Hydro seat A"
        # - testId 3: keep actual name from SAP/payload
        # - testId 4: force "Air seat A"
        # - B variants: force B names
        if tid_int == 2:
            tn = "Hydro seat A"
        elif tid_int == 29:
            tn = "Hydro seat B"
        elif tid_int == 4:
            tn = "Air seat A"
        elif tid_int == 49:
            tn = "Air seat B"
        td = _to_float(filtered_duration[i])
        tp = _to_float(filtered_pressure[i])

        # Pressure conversion
        if pressureunit.lower() == "psi":
            testing_pressure_psi = tp
            testing_pressure_bar = tp / 14.5
        else:
            testing_pressure_bar = tp
            testing_pressure_psi = tp * 14.5

        testing_duration_unit = "Sec"
        testing_duration_minutes = td / 60
        testing_pressure_kgcm2 = testing_pressure_bar

        with connection.cursor() as cursor:
            def _fetch_test_meta_rows(test_type_id: int):
                cursor.execute("""
                    SELECT c.TEST_CATEGORY_MEDIUM, tt.TEST_CATEGORY_ID, c.PRESSURE_COLUMN_NAME, c.DURATION_COLUMN_NAME
                    FROM test_type tt
                    JOIN category c ON tt.TEST_CATEGORY_ID = c.TEST_CATEGORY_ID
                    WHERE tt.TEST_TYPE_ID = %s
                """, [test_type_id])
                return cursor.fetchall()

            rows = _fetch_test_meta_rows(tid)
            if not rows:
                # Some SAP flows add "B" variants (ex: 29, 49) that might not exist in test_type table.
                # Fallback: reuse metadata from base test IDs but still save under the requested tid.
                # Fallback metadata source for B-variants:
                # 29 uses same category/meta as base testId 2
                # 49 uses same category/meta as base testId 4
                fallback_map = {29: 2, 49: 4}
                fallback_id = fallback_map.get(int(tid))
                if fallback_id is not None:
                    rows = _fetch_test_meta_rows(int(fallback_id))

            if not rows:
                # Still unknown test id (not configured in DB).
                # Do NOT skip: user wants to save/show all tests coming from SAP.
                # Use safe defaults for meta fields.
                rows = [("UNKNOWN", 0, "", "")]

            for row in rows:
                # Check if TEST_ID exists (where VALVE_SERIAL_NO IS NULL - common test data)
                cursor.execute(
                    "SELECT COUNT(*) FROM temp_testing_data WHERE TEST_ID = %s AND VALVE_SERIAL_NO IS NULL",
                    [tid]
                )
                exists = cursor.fetchone()[0]

                if exists:
                    # Update existing row
                    cursor.execute("""
                        UPDATE temp_testing_data SET
                            TEST_NAME = %s,
                            TEST_MEDIUM = %s,
                            TEST_CATEGORY = %s,
                            COL_PRE = %s,
                            COL_DUR = %s,
                            TESTING_PR_UNIT = %s,
                            TESTING_PR_BAR = %s,
                            TESTING_PR_PSI = %s,
                            TESTING_PR_KGCM2 = %s,
                            TESTING_DUR_UNIT = %s,
                            TESTING_DUR_SEC = %s,
                            TESTING_DUR_MIN = %s
                        WHERE TEST_ID = %s AND VALVE_SERIAL_NO IS NULL
                    """, [
                        tn, row[0], row[1], row[2], row[3],
                        pressureunit,
                        testing_pressure_bar, testing_pressure_psi, testing_pressure_kgcm2,
                        testing_duration_unit, td, testing_duration_minutes,
                        tid
                    ])
                else:
                    # Insert new row (VALVE_SERIAL_NO will be NULL)
                    cursor.execute("""
                        INSERT INTO temp_testing_data 
                        (VALVE_SERIAL_NO,TEST_ID,TEST_NAME,TEST_MEDIUM,TEST_CATEGORY,COL_PRE,COL_DUR,
                        TESTING_PR_UNIT,TESTING_PR_BAR,TESTING_PR_PSI,TESTING_PR_KGCM2,
                        TESTING_DUR_UNIT,TESTING_DUR_SEC,TESTING_DUR_MIN)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, [
                        None,  # VALVE_SERIAL_NO = NULL for common test data
                        tid, tn, row[0], row[1], row[2], row[3],
                        pressureunit,
                        testing_pressure_bar, testing_pressure_psi, testing_pressure_kgcm2,
                        testing_duration_unit, td, testing_duration_minutes
                    ])
