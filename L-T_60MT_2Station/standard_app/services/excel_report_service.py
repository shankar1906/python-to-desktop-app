import os
import openpyxl
import re
from django.db import connection
from datetime import datetime

def generate_excel_report(valve_serial_no, count_id, station_id):
    """
    Generates an Excel Report based on the template 'gcc report format.xlsx'
    Mappping database values directly into explicit cells.
    """
    try:
        template_path = os.path.join(os.path.dirname(__file__), '..', 'excel', 'l-and-t-10mt-2-station.xlsx')
        if not os.path.exists(template_path):
            print("[EXCEL] Template file not found")
            return None

        # Load the workbook
        wb = openpyxl.load_workbook(template_path)
        ws = wb.active
        bar_2_psi = 14.5

        with connection.cursor() as cursor:
            # 1. Fetch common metadata from pressure_analysis
            # Standardized column order:
            # 0:VALVESIZE_NAME, 1:VALVETYPE_NAME, 2:VALVECLASS_NAME, 3:STANDARD_NAME, 4:SHELLMATERIAL_NAME,
            # 5:TEST_ID, 6:TEST_NAME, 7:SET_PRESSURE, 8:SET_TIME, 9:START_PRESSURE, 10:ACTUAL_PRESSURE,
            # 11:VALVE_STATUS, 12:CYCLE_COMPLETED_DATE, 13:PRESSURE_UNIT, 14:DURATION_TYPE, 
            # 15:TESTED_BY, 16:APPROVED_BY
            # 1. Fetch main test data and all dynamic columns from pressure_analysis
            cursor.execute('''
                SELECT *
                FROM pressure_analysis
                WHERE VALVE_SER_NO = %s AND COUNT_ID = %s
            ''', [valve_serial_no, count_id])
            test_rows = cursor.fetchall()
            
            if not test_rows:
                return None
                
            # Use cursor.description to map columns to indices dynamically
            col_names = [desc[0] for desc in cursor.description]
            row_dict_main = dict(zip(col_names, test_rows[0]))
            
            valve_size = row_dict_main.get('VALVESIZE_NAME') or ""
            valve_type = row_dict_main.get('VALVETYPE_NAME') or ""
            valve_class = row_dict_main.get('VALVECLASS_NAME') or ""
            standard = row_dict_main.get('STANDARD_NAME') or ""
            shell_material = row_dict_main.get('SHELLMATERIAL_NAME') or ""
            completed_date = row_dict_main.get('CYCLE_COMPLETED_DATE')
            
            # Extract extra_data from COL1-COL65 in pressure_analysis
            extra_data = {}
            for i in range(1, 66):
                name_key = f'COL{i}_NAME'
                value_key = f'COL{i}_VALUE'
                name_val = row_dict_main.get(name_key)
                value_val = row_dict_main.get(value_key)
                
                if name_val and isinstance(name_val, str):
                    # Robust normalization matching the save API
                    std_key = re.sub(r'[^A-Z0-9]', '_', name_val.upper()).strip('_').lower()
                    while '__' in std_key:
                        std_key = std_key.replace('__', '_')
                    extra_data[std_key] = value_val
            
            # Format Date & Time
            date_str = ""
            time_str = ""
            if completed_date:
                # Handle string or datetime type dynamically depending on DB engine
                if isinstance(completed_date, str):
                    try:
                        dt = datetime.strptime(completed_date, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        dt = None
                else:
                    dt = completed_date
                    
                if dt:
                    date_str = dt.strftime('%d/%m/%Y')
                    time_str = dt.strftime('%H:%M:%S')

            # Extra data is now fetched from pressure_analysis to ensure historical accuracy
            
            # ----------------------------------------------------
            # Map Base Values to Template
            # ----------------------------------------------------
            def get_anchor(cell_id):
                for merged_range in ws.merged_cells.ranges:
                    if cell_id in merged_range:
                        return merged_range.coord.split(':')[0]
                return cell_id

            def set_cell_optional(cell_id, val):
                """Write value to cell; None clears so null DB fields do not crash and stale template text is removed."""
                target = get_anchor(cell_id)
                if val is None or val == "":
                    ws[target] = None
                else:
                    ws[target] = val

            def assign_val(cell_id, *vals, sep=","):
                # Filter out empty values and join them
                val_list = [str(v).strip() for v in vals if v is not None and str(v).strip()]
                if not val_list: return
                val = sep.join(val_list)
                
                target_cell = get_anchor(cell_id)
                        
                current_val = ws[target_cell].value
                if current_val is None:
                    current_val = ""
                else:
                    current_val = str(current_val).strip()
                
                if current_val:
                    if val not in current_val:
                        # If we're appending to existing content, use the separator
                        ws[target_cell] = current_val + sep + val
                else:
                    ws[target_cell] = val
                    
            # Header Mapping
            assign_val('E4', extra_data.get('sale_order_no', ''))
            assign_val('E5', extra_data.get('sale_item_no', ''))
            assign_val('E6', extra_data.get('gad_no', ''))
            
            assign_val('K4', valve_size)
            assign_val('K5', valve_class)
            assign_val('K6', valve_serial_no)
            assign_val('K7', extra_data.get('end_details', ''))
            assign_val('K8', shell_material)

            assign_val('U4', extra_data.get('date', date_str))
            assign_val('U5', extra_data.get('shift', ''))
            assign_val('U6', extra_data.get('gauge_detail', ''))
            assign_val('A13', extra_data.get('antistatic_test_result', ''), sep='\n')

            # Heat Numbers / RT / MPI (Rows 9-11)
            # Body/Shell
            assign_val('A9', extra_data.get('body_heat_no'), extra_data.get('body_mpi_dp_no'), extra_data.get('body_rt_no'),sep=",")
            # Connector(L) / Bonnet
            assign_val('D9', extra_data.get('connector_l_heat_no'), extra_data.get('connector_l_mpi_dp_no'), extra_data.get('connector_l_rt_no'),sep=",")
            # Connector(R) / Extn
            assign_val('G9', extra_data.get('connector_r_heat_no'), extra_data.get('connector_r_mpi_dp_no'), extra_data.get('connector_r_rt_no'),sep=",")
        

            # Gear / Actuator
            assign_val('K9', extra_data.get('gear_unit_detail', extra_data.get('gear_unit_details', '')))
            assign_val('K11', extra_data.get('actuator_detail', extra_data.get('actuator_details', '')))

            # Antistatic Test (Resistance < 10 Ohm)
            assign_val('B16', extra_data.get('body_to_ball_power', ''))
            assign_val('C16', extra_data.get('body_to_ball_resistance', ''))
            assign_val('B17', extra_data.get('body_to_stem_power', ''))
            assign_val('C17', extra_data.get('body_to_stem_resistance', ''))
 
            # Drying and testing
            ws['P27'] = '✔' if extra_data.get('drying_technique_compressed_air') == 'True' else '☐'
            ws['P28'] = '✔' if extra_data.get('drying_technique_vacuum') == 'True' else '☐'

            assign_val('A26', extra_data.get('remarks', ''), sep='\n')
            assign_val('I26', extra_data.get('water_temperature_result',""), sep='\n')
            assign_val('Q27', extra_data.get('drying_result',''))
            assign_val('S27', extra_data.get('abnormal_sound_result',''))
            assign_val('U27', extra_data.get('water_draining_result',''))
            assign_val('C28', extra_data.get('drain_plug_torque'))
            assign_val('G28', extra_data.get('vent_plug_torque'))
            assign_val('A20', extra_data.get('torque_setting_close_open',''))
            assign_val('C20', extra_data.get('torque_setting_open_close', ''))
            assign_val('E20', extra_data.get('actuator_timing_close_open',''))
            assign_val('F20', extra_data.get('actuator_timing_open_close', ''))
            assign_val('G20', extra_data.get('actuator_sizing_pressure', ''))
            assign_val('I27', extra_data.get('seat_test_stabilization_time', ''), sep='\n')

            # Vent Test (Column F)
            assign_val('F15', extra_data.get('seat_test_vent_set_pressure', ''))
            assign_val('F16', extra_data.get('seat_test_vent_actual_pressure', ''))
            assign_val('F17', extra_data.get('seat_test_vent_duration_min', ''))

            # Drain Test (Column G)
            assign_val('G15', extra_data.get('seat_test_drain_set_pressure', ''))
            assign_val('G16', extra_data.get('seat_test_drain_actual_pressure', ''))
            assign_val('G17', extra_data.get('seat_test_drain_duration_min', ''))

            # Torque Values (Actual and Required)
            assign_val('N15', extra_data.get('torque_bto_dbb_required', ''))
            assign_val('N16', extra_data.get('torque_bto_dbb_actual', ''))
            assign_val('O15', extra_data.get('torque_bto_connector_l_required', ''))
            assign_val('O16', extra_data.get('torque_bto_connector_l_actual', ''))
            assign_val('P15', extra_data.get('torque_bto_connector_r_required', ''))
            assign_val('P16', extra_data.get('torque_bto_connector_r_actual', ''))
            assign_val('Q15', extra_data.get('torque_btc_required', ''))
            assign_val('Q16', extra_data.get('torque_btc_actual', ''))

            # Run Torque (Column T)
            # assign_val('T15', extra_data.get('run_torque_set', ''))
            # assign_val('T16', extra_data.get('run_torque_result', ''))
            # assign_val('T17', 'OK' if extra_data.get('run_torque_result') else '')

            # Antistatic Test Results (Row 33-34)
            assign_val('I33', extra_data.get('body_to_ball_resistance', ''))
            assign_val('I34', extra_data.get('body_to_stem_resistance', ''))

            # Signatures (Tested by / Witnessed by)
            assign_val('L19', extra_data.get('tested_by',''))
            assign_val('P19', extra_data.get('witnessed_by',''))

            assign_val('S19', extra_data.get('gear_unit_stopper_torque',''))


            stem_position = extra_data.get('stem_position', '')
            if stem_position == 'Vertical':
                assign_val('V19', '✔')
            else:
                assign_val('V20', '✔')    
            # The loop above now handles the main grid mapping
            # ----------------------------------------------------
            # Map Test Run Grids
            # ----------------------------------------------------
            def get_result_text(status):
                if status is None: return ""
                return "PASS" if str(status).strip().upper() == "PASS" else "FAIL"

            # Pre-calculate valve inch for possible future use
            def get_inch(s):
                if not s: return 0
                import re
                match = re.search(r"(\d+(?:\.\d+)?)", str(s))
                return float(match.group(1)) if match else 0
            
            valve_inch = get_inch(valve_size)

            def safe_float(v):
                if v is None or v == "":
                    return None
                try:
                    return float(v)
                except (TypeError, ValueError):
                    return None

            all_test_results = []
            for test in test_rows:
                test_id = test[2]
                t_name = test[3]
                status_raw = test[26]
                
                if status_raw:
                    s_val = str(status_raw).strip().upper()
                    if s_val in ("PASS", "FAIL"):
                        all_test_results.append(s_val)

                # Map Test ID to Column (only if status is not Null)
                col = None
                print(status_raw, "--------------------------------")
                if status_raw:
                    if test_id in (6,30): # Shell Test
                        col = 'E'
                    elif test_id in (2, 29): # Double block and Bleed test
                        col = 'H'
                    elif test_id in (3,31): # Seat L 
                        col = 'J'
                    elif test_id in (4,32): # Seat R
                        col = 'K'
                    elif test_id in (8,33): # DIB1 & DIB2
                        col = 'L'
                    elif test_id in (1,34): # Cavity Relief L
                        col = 'S'
                    elif test_id in (7,35): # Cavity Relief R
                        col = 'T'

                p_unit = str(test[7] or "").lower().strip()
                
                if col:
                    # Set Pressure: Convert to PSI if stored in bar
                    set_p_raw = safe_float(test[5])
                    if p_unit == 'psi':
                        set_pressure = set_p_raw
                    else:
                        set_pressure = (set_p_raw * 14.5) if set_p_raw is not None else None
                        
                    # Duration: Convert seconds to minutes
                    duration_sec = safe_float(test[8])
                    duration_min = (duration_sec / 60) if duration_sec is not None else None
                    
                    result = get_result_text(test[26])

                    if test_id in (1,41):
                        ws[f'{col}15'] = f"{set_pressure} \n {duration_min} \n {result}"
                    else:
                        ws[f'{col}15'] = set_pressure
                        ws[f'{col}16'] = duration_min
                        ws[f'{col}17'] = result
                    
                    
                 
            
            # Overall Result logic for I19
            if all_test_results:
                final_status = "FAIL" if "FAIL" in all_test_results else "PASS"
                assign_val('I19', final_status)
                
            # Test results are now mapped in the loop above
            # Fetch Gauges with detailed fields
            cursor.execute("""
                SELECT GD_SERIAL_NUMBER, GD_MEDIUM, GD_DUE_DATE, 
                       PRESSURE_UNIT, GD_PRESSURE_RANGE_PSI, 
                       GD_PRESSURE_RANGE_BAR, GD_PRESSURE_RANGE_KG_CM2
                FROM gauge_details_test_log
                WHERE VALVE_SERIAL_NUMBER = %s AND GD_STATION_ID = %s
            """, [valve_serial_no, str(station_id)])
            gauge_rows = cursor.fetchall()

            if gauge_rows:
                all_serials = []
                all_ranges = []
                all_dues = []

                for row in gauge_rows:
                    gd_serial = row[0]
                    gd_due = row[2]
                    gd_unit = (row[3] or "").upper()
                    gd_range_psi = str(row[4] or "").strip()
                    gd_range_bar = str(row[5] or "").strip()
                    gd_range_kg = str(row[6] or "").strip()

                    # Determine correct range based on unit
                    raw_range = ""
                    if gd_unit == "PSI": raw_range = gd_range_psi
                    elif gd_unit == "BAR": raw_range = gd_range_bar
                    elif "KG" in gd_unit: raw_range = gd_range_kg
                    else: raw_range = gd_range_psi or gd_range_bar

                    # Format range: avoid "0 - 0-2000" if "0-" is already present
                    if raw_range:
                        clean_range = raw_range
                        if "-" not in raw_range and raw_range.lower() != "none":
                            clean_range = f"0 - {raw_range}"
                        all_ranges.append(f"{clean_range} {gd_unit}")
                    
                    if gd_serial:
                        all_serials.append(str(gd_serial))
                    
                    if gd_due:
                        if isinstance(gd_due, str):
                            try:
                                d_str = datetime.strptime(gd_due, '%Y-%m-%d').strftime('%d/%m/%Y')
                            except ValueError:
                                d_str = gd_due
                        else:
                            d_str = gd_due.strftime('%d/%m/%Y')
                        all_dues.append(d_str)

                # Map to P7, R7, U7 with newlines
                # assign_val uses get_anchor so it will target the merged cell start
                ws[get_anchor('P7')] = "\n".join(all_serials)
                ws[get_anchor('R7')] = "\n".join(all_ranges)
                ws[get_anchor('U7')] = "\n".join(all_dues)

            # Fetch Instruments
            cursor.execute("""
                SELECT INSTRUMENT_SERIAL_NUMBER, INSTRUMENT_TYPE, INSTRUMENT_DUE_DATE
                FROM instrument_test_log
                WHERE VALVE_SERIAL_NUMBER = %s
            """, [valve_serial_no])
            inst_rows = cursor.fetchall()

            # ----------------------------------------------------
            # Map Instruments to Rows 23-25 (Two Columns)
            # ----------------------------------------------------
            # Left column: A, D, G | Right column: K, P, S
            inst_mapping = [
                ('A23', 'D23', 'G23'), ('A24', 'D24', 'G24'), ('A25', 'D25', 'G25'),
                ('K23', 'P23', 'S23'), ('K24', 'P24', 'S24'), ('K25', 'P25', 'S25')
            ]

            for i, row in enumerate(inst_rows[:6]):
                type_cell, ser_cell, due_cell = inst_mapping[i]
                
                i_ser = row[0]
                i_type = row[1]
                i_due = row[2]
                
                assign_val(type_cell, i_type)
                assign_val(ser_cell, i_ser)
                
                # Format Due Date
                i_due_str = ""
                if i_due:
                    if isinstance(i_due, str):
                        try:
                            i_due_str = datetime.strptime(i_due, '%Y-%m-%d').strftime('%d/%m/%Y')
                        except ValueError:
                            i_due_str = i_due
                    else:
                        i_due_str = i_due.strftime('%d/%m/%Y')
                assign_val(due_cell, i_due_str)

        # Generate output file
        export_dir = "S:/Reports"
        os.makedirs(export_dir, exist_ok=True)
        filename = f"{valve_serial_no}_Count-{count_id}_report.xlsx"
        filepath = os.path.join(export_dir, filename)
        
        wb.save(filepath)
        print(f"[EXCEL] Generated report: {filepath}")
        
        # Return URL-ready path or direct file
        return f"/api/cycle_complete/download_excel/?file={filename}"

    except Exception as e:
        print(f"[EXCEL] Error generating excel report: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_excel_report(valve_serial_no, count_id, station_id):
    """
    Test function to run generate_excel_report directly.
    """
    print("=" * 50)
    print(f"Testing generate_excel_report with:")
    print(f"  Valve Serial No: {valve_serial_no}")
    print(f"  Count ID:        {count_id}")
    print(f"  Station ID:      {station_id}")
    print("=" * 50)
    
    result = generate_excel_report(valve_serial_no, count_id, station_id)
    
    if result:
        print(f"\n[SUCCESS] Report generated successfully!")
        print(f"File endpoint/path: {result}")
    else:
        print(f"\n[FAILED] Failed to generate report. Check if data exists for these parameters.")

if __name__ == '__main__':
    import sys
    import os
    import django

    # 1. Setup Django environment to allow database access outside of normal flow
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up to the root project folder (L-T-10MT-KPM-4Station-2026)
    project_root = os.path.dirname(os.path.dirname(current_dir))
    sys.path.append(project_root)
    
    # Set the default Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'standard_soft.settings')
    # Initialize Django
    django.setup()

    # 2. Parse command-line arguments or use defaults
    if len(sys.argv) == 4:
        test_valve = sys.argv[1]
        test_count = sys.argv[2]
        test_station = sys.argv[3]
        test_excel_report(test_valve, test_count, test_station)
    else:
        print("Usage: python excel_report_service.py <valve_serial_no> <count_id> <station_id>")
        print("Example: python excel_report_service.py V12345 1 1")
        print("\nRunning with dummy values for demonstration...")
        
        # You can also hardcode your test values here if you prefer not to use CLI arguments
        test_valve = "TEST_VALVE_001"
        test_count = "1"
        test_station = "1"
        
        test_excel_report(test_valve, test_count, test_station)