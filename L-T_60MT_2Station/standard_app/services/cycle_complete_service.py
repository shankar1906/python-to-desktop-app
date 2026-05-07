from django.db import connection
from standard_app.views.db_download import export_DB
from standard_app.services.excel_report_service import generate_excel_report
from standard_app.services.livepage_service import truncate_currentstatus_service
from standard_app.services.sap_service import sap_upload_doc

def save_station_service(station_id, extra_fields):
    """
    Saves extra fields into specifically assigned COL{i}_NAME and COL{i}_VALUE 
    for the given station in the master_temp_data table.
    """
    with connection.cursor() as cursor:
        mapping = {
            # FBV Specific
            "body_ball_power": 20,
            "body_stem_power": 21,
            "timing_close_open": 22,
            "timing_open_close": 23,
            "torque_close_open": 24,
            "torque_open_close": 25,
            "run_torque": 26,
            "torque_lh": 27,
            "torque_rh": 28,
            "gear_unit_stopper": 29,
            "measured_power": 30,
            "technique_result": 31,
            "check_sound": 32,
            "draining_test": 33,
            
            # TMBV Specific
            "body_to_ball_power": 20,
            "body_to_ball_resistance": 21,
            "body_to_stem_power": 22,
            "body_to_stem_resistance": 23,
            "actuator_timing_close_open": 24,
            "actuator_timing_open_close": 25,
            "torque_setting_close_open": 26,
            "torque_setting_open_close": 27,
            "actuator_sizing_pressure": 28,
            "run_torque_set": 29,
            "run_torque_result": 30,
            "gear_unit_stopper_torque": 31,
            "drying_technique_compressed_air": 32,
            "drying_technique_vacuum": 33,
            "abnormal_sound_result": 34,
            "water_draining_result": 35,
            "drying_result": 36,
            "gear_unit_details": 37,
            "actuator_details": 38,
            "antistatic_test_result": 39,
            "water_temperature_result": 40,
            "seat_test_stabilization_time": 41,
            "drain_plug_torque": 42,
            "vent_plug_torque": 43,
            "stem_position": 44,
            "seat_test_vent_set_pressure": 46,
            "seat_test_drain_set_pressure": 47,
            "seat_test_vent_actual_pressure": 48,
            "seat_test_drain_actual_pressure": 49,
            "seat_test_vent_duration_min": 50,
            "seat_test_drain_duration_min": 51,
            "torque_bto_dbb_required": 52,
            "torque_bto_dbb_actual": 53,
            "torque_bto_connector_l_required": 54,
            "torque_bto_connector_l_actual": 55,
            "torque_bto_connector_r_required": 56,
            "torque_bto_connector_r_actual": 57,
            "torque_btc_required": 58,
            "torque_btc_actual": 59,
            
            # Shared
            "remarks": 45
        }
        
        updates = []
        params = []
        
        for key, col_num in mapping.items():
            if key in extra_fields:
                updates.append(f"COL{col_num}_NAME = %s")
                updates.append(f"COL{col_num}_VALUE = %s")
                params.extend([key, extra_fields[key]])
        
        if updates:
            query = f"UPDATE master_temp_data SET {', '.join(updates)} WHERE ID = %s"
            params.append(station_id)
            cursor.execute(query, params)
            
            # Also push the mapped metadata directly to temp_pressure_analysis 
            # so the final global save can carry it properly.
            cursor.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE ID = %s", [station_id])
            valve_ser_no_row = cursor.fetchone()
            if valve_ser_no_row:
                valve_ser_no = valve_ser_no_row[0]
                t_params = params[:-1] + [valve_ser_no]
                t_query = f"UPDATE temp_pressure_analysis SET {', '.join(updates)} WHERE VALVE_SER_NO = %s"
                cursor.execute(t_query, t_params)
            
            connection.commit()
            
    return True

def global_save_service():
    """
    Finalizes the cycle complete:
    1. Transfers temp_pressure_analysis to pressure_analysis.
    2. Increments serial_tbl count.
    3. Exports DB/PDF.
    4. Truncates temp_pressure_analysis.
    5. Disables active stations.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT VALVE_SER_NO, TEST_ID, COUNT_ID FROM temp_pressure_analysis")
        result = cursor.fetchall()
        
        cursor.execute("SELECT ID, VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS = 'Enabled'")
        active_stations = cursor.fetchall()
        
        if not result:
            return False # Nothing to save
            
        processed_serials = set()
        ser_to_count = {row[0]: row[2] for row in result}
        
        # Build column map spanning 1 to 65
        cols = []
        for i in range(1, 66):
            cols.append(f"COL{i}_NAME")
            cols.append(f"COL{i}_VALUE")
        col_str = ", ".join(cols)

        # 1. Transfer to pressure_analysis
        cursor.execute(f"""
            INSERT INTO pressure_analysis (
                TEST_ID, TEST_NAME, SET_PRESSURE, SET_TIME, VALVE_SER_NO, PRESSURE_UNIT, STANDARD_NAME,
                VALVESIZE_NAME, VALVECLASS_NAME, VALVETYPE_NAME, SHELLMATERIAL_NAME,
                {col_str}, COUNT_ID,
                START_PRESSURE, START, RESULT_PRESSURE, END, ACTUAL_PRESSURE, VALVE_STATUS, CYCLE_COMPLETE, DURATION_TYPE
            )
            SELECT 
                TEST_ID, TEST_NAME, SET_PRESSURE, SET_TIME, VALVE_SER_NO, PRESSURE_UNIT, STANDARD_NAME,
                VALVESIZE_NAME, VALVECLASS_NAME, VALVETYPE_NAME, SHELLMATERIAL_NAME,
                {col_str}, COUNT_ID,
                START_PRESSURE, START, RESULT_PRESSURE, END, ACTUAL_PRESSURE, VALVE_STATUS, 'Yes', DURATION_TYPE
            FROM temp_pressure_analysis
        """)
        
        # 2. Increment Serial count
        for row in result:
            serial_v = row[0]
            if serial_v not in processed_serials:
                cursor.execute("SELECT Serial_No FROM serial_tbl WHERE Serial_No = %s", [serial_v])
                serial_no = cursor.fetchone()
                if serial_no:
                    cursor.execute("UPDATE serial_tbl set Count_No = Count_No + 1 WHERE Serial_No = %s", [serial_v])
                else:
                    cursor.execute("INSERT INTO serial_tbl (Serial_No, Count_No) VALUES (%s, %s)", [serial_v, 1])
                processed_serials.add(serial_v)

        # 3. Export DB to PDF & Excel
        excel_urls = []
        for station_id, valve_ser_no in active_stations:
            count_id = ser_to_count.get(valve_ser_no)
            if count_id is not None:
                try:
                    export_DB(valve_ser_no, count_id, station_id)
                except Exception as e:
                    print(f"Error exporting DB for station {station_id}: {e}")
                
                try:
                    excel_url = generate_excel_report(valve_ser_no, count_id, station_id)
                    if excel_url:
                        excel_urls.append(excel_url)
                except Exception as e:
                    print(f"Error generating Excel for station {station_id}: {e}")

                # 3.1 SAP Upload for both PDF and Excel reports
                try:
                    pdf_filename = f"/{valve_ser_no}_Count-{count_id}_report.pdf"
                    excel_filename = f"/{valve_ser_no}_Count-{count_id}_report.xlsx"
                    
                    print(f"--- Triggering SAP Upload for {valve_ser_no} ---")
                    sap_upload_doc(file=pdf_filename, serial_no=valve_ser_no)
                    sap_upload_doc(file=excel_filename, serial_no=valve_ser_no)
                except Exception as e:
                    print(f"Error in SAP upload trigger for {valve_ser_no}: {e}")

        # 4. Truncate temp table
        cursor.execute("TRUNCATE TABLE temp_pressure_analysis")
        truncate_currentstatus_service()
        
        # 5. Disable stations and clear extra data fields
        if active_stations:
            valve_ser_nos = [row[1] for row in active_stations]
            placeholders = ','.join(['%s'] * len(valve_ser_nos))
            
            # Build SET clause to clear COL1_NAME through COL64_VALUE
            cols_to_clear = []
            for i in range(1, 66):
                cols_to_clear.append(f"COL{i}_NAME=''")
                cols_to_clear.append(f"COL{i}_VALUE=''")
            clear_clause = ", ".join(cols_to_clear)
            
            cursor.execute(f"UPDATE master_temp_data SET STATION_STATUS = 'Disabled', CYCLE_COMPLETE = 'Yes', {clear_clause} WHERE VALVE_SER_NO IN ({placeholders})", valve_ser_nos)
        
        connection.commit()
    return {"success": True, "excel_urls": excel_urls}
