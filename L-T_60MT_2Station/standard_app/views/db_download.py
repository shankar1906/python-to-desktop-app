import os
from openpyxl import Workbook
from django.db import connection
from openpyxl import load_workbook
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML

def export_DB(valve_serial_no, count_id, station_num):
    """
    Export current_status_stationX table data to E drive as Excel file
    """
    try:

        DB_Name = {
            1: "current_status_station1",
            2: "current_status_station2",
            3: "current_status_station3",
        }

        # Validate station number
        table_name = DB_Name.get(station_num)
        if not table_name:
            raise ValueError("Invalid station number")

        # Create directory if not exists
        e_drive_path = "S:/LandT-10MT-KPM_DB_export"
        os.makedirs(e_drive_path, exist_ok=True)

        filename = f"{valve_serial_no}_Count-{count_id}.xlsx"
        filepath = os.path.join(e_drive_path, filename)

        with connection.cursor() as cursor:

            # Use f-string for table name
            query = f"""
                SELECT ID, VALVE_SERIAL_NO, PRESSURE, TEST_ID, TEST_NAME,
                       DATE_TIME, TIMER_STATUS, RESULT
                FROM {table_name}
                WHERE VALVE_SERIAL_NO = %s
                ORDER BY ID
            """

            cursor.execute(query, [valve_serial_no])

            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

        # Create Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = f"Station {station_num} Data"

        ws.append(columns)

        for row in rows:
            ws.append(row)

        # Auto width
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[column_letter].width = max_length + 2

        wb.save(filepath)
        generate_graph(filepath, valve_serial_no, station_num, count_id)
        return True

    except Exception as e:
        print(f"[EXPORT] Failed to export data: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_graph_base64_for_test(excel_filepath, test_id, test_name):
    # This was the logic from generate_graph but specifically for ONE test
    try:
        wb = load_workbook(excel_filepath)
        ws = wb.active

        date_times = []
        pressures = []
        timer_status = []

        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[3] == test_id:
                date_time = row[5]
                pressure = row[2]
                timer_stat = row[6]

                if date_time and pressure is not None:
                    if isinstance(date_time, str):
                        try:
                            date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                        except:
                            continue

                    date_times.append(date_time)
                    pressures.append(float(pressure))
                    timer_status.append(int(timer_stat) if timer_stat is not None else 0)

        if not date_times:
            wb.close()
            return None

        # ---------------- TIMER CHECK ----------------
        has_timer_on = any(s == 1 for s in timer_status)
        has_timer_off_after_on = False

        timer_was_on = False
        for s in timer_status:
            if s == 1:
                timer_was_on = True
            elif s == 0 and timer_was_on:
                has_timer_off_after_on = True
                break

        if not has_timer_on or not has_timer_off_after_on:
            wb.close()
            return None

        # ---------------- FIND TIMER WINDOW ----------------
        timer_start_time = None
        timer_stop_time = None

        for i in range(len(timer_status)):
            if timer_status[i] == 1 and timer_start_time is None:
                timer_start_time = date_times[i]

            if timer_start_time and timer_status[i] == 0:
                timer_stop_time = date_times[i]
                break

        # ---------------- MODERN FIGURE ----------------
        fig, ax = plt.subplots(figsize=(16, 5), dpi=300)
        
        # Modern Color Palette
        COLOR_BG = '#FFFFFF'
        COLOR_PLOT_BG = '#FFFFFF'
        COLOR_PRIMARY = '#2563EB'  # Vibrant Blue (Royal Blue)
        COLOR_GRID = '#E2E8F0'     # Light Slate
        COLOR_TEXT = '#475569'     # Slate 600
        COLOR_TITLE = '#1E293B'    # Slate 800
        COLOR_START = '#10B981'    # Emerald 500
        COLOR_STOP = '#EF4444'     # Red 500

        # Background Configuration
        fig.patch.set_facecolor(COLOR_BG)
        ax.set_facecolor(COLOR_PLOT_BG)

        # ---------------- PRESSURE LINE ----------------
        ax.plot(
            date_times,
            pressures,
            color=COLOR_PRIMARY,
            linewidth=2.5,
            solid_capstyle='round',
            zorder=3,
        )

        # Soft Gradient Fill
        ax.fill_between(
            date_times,
            pressures,
            0,
            color=COLOR_PRIMARY,
            alpha=0.10,
            zorder=2
        )

        # ---------------- TIMER MARKERS ----------------
        y_min, y_max = ax.get_ylim()
        
        ax.axvline(x=timer_start_time, color=COLOR_START, linestyle='--', linewidth=1.5, zorder=4)
        ax.axvline(x=timer_stop_time, color=COLOR_STOP, linestyle='--', linewidth=1.5, zorder=4)

        ax.text(timer_start_time, y_max, f'START - {timer_start_time}', color=COLOR_START, fontsize=10, fontweight='bold', va='top', ha='right', rotation=90)
        ax.text(timer_stop_time, y_max, f'STOP - {timer_stop_time}', color=COLOR_STOP, fontsize=10, fontweight='bold', va='top', ha='right', rotation=90)

        ax.axvspan(
            timer_start_time,
            timer_stop_time,
            color=COLOR_START,
            alpha=0.05,
            zorder=1
        )

        # ---------------- AXIS STYLING ----------------
        # ax.set_title(test_name, fontsize=16, fontweight='bold', color=COLOR_TITLE, pad=20)
        ax.set_xlabel('Time', fontsize=11, fontweight='500', color=COLOR_TEXT, labelpad=10)
        ax.set_ylabel('Pressure', fontsize=11, fontweight='500', color=COLOR_TEXT, labelpad=10)

        # Date/Time Formatting
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=6, maxticks=10))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        
        ax.grid(True, axis='y', color=COLOR_GRID, linestyle='-', linewidth=0.5, alpha=0.8)
        ax.grid(False, axis='x')
        ax.set_axisbelow(True)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color(COLOR_GRID)
        ax.spines['bottom'].set_linewidth(1.5)

        ax.tick_params(axis='both', colors=COLOR_TEXT, labelsize=10)
        ax.tick_params(axis='y', length=0)
        ax.tick_params(axis='x', length=5, color=COLOR_GRID)
        
        fig.autofmt_xdate(rotation=45, ha='right')
        ax.margins(x=0.02, y=0.1)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(
            buffer,
            format='png',
            dpi=200,
            bbox_inches='tight',
            facecolor='white'
        )
        buffer.seek(0)

        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        plt.close(fig)
        buffer.close()
        wb.close()

        return f"data:image/png;base64,{image_base64}"

    except Exception as e:
        print(f"[GRAPH] Error generating graph for test {test_id}: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_graph(excel_filepath, valve_serial_no, station_num, count_id):
    """
    Generate modern, professional pressure vs time graph for ALL tests from Excel file
    and combine them into a PDF report using graph_report_template.html
    """
    try:
        current_date_str = datetime.now().strftime("%d-%m-%Y")

        with connection.cursor() as cursor:
            # Fetch master data for the valve (common for all tests)
            cursor.execute('''
                SELECT VALVE_SER_NO, VALVESIZE_NAME, VALVETYPE_NAME, VALVECLASS_NAME, SHELLMATERIAL_NAME,
                TEST_NAME,VALVE_STATUS,
                COL9_VALUE,COL10_VALUE,COL11_VALUE,
                COL12_VALUE,COL13_VALUE,COL14_VALUE,
                COL15_VALUE,COL16_VALUE,COL17_VALUE,
                COL18_VALUE
                FROM pressure_analysis
                WHERE VALVE_SER_NO = %s AND COUNT_ID = %s
                LIMIT 1
            ''', [valve_serial_no, count_id])
            
            master_row = cursor.fetchone()
            if not master_row:
                print(f"[PDF] No master data found for valve {valve_serial_no}")
                return False
            
            # Fetch all test data
            cursor.execute('''
                SELECT TEST_ID, TEST_NAME, SET_TIME, SET_PRESSURE, 
                       PRESSURE_UNIT, START_PRESSURE, ACTUAL_PRESSURE, VALVE_STATUS
                FROM pressure_analysis
                WHERE VALVE_SER_NO = %s AND COUNT_ID = %s
                ORDER BY TEST_ID ASC
            ''', [valve_serial_no, count_id])
            
            test_rows = cursor.fetchall()

            # also tested_by is needed... we can try to fetch it from pressure_analysis
            tested_by = master_row[16] if master_row and len(master_row) > 16 else ""
            
            if not tested_by:
                # Fallback to master_temp_data
                cursor.execute('''
                    SELECT COL18_VALUE FROM master_temp_data WHERE VALVE_SER_NO = %s
                    LIMIT 1
                ''', [valve_serial_no])
                temp_row = cursor.fetchone()
                tested_by = temp_row[0] if temp_row else ""

        if not test_rows:
            return False

        valve_size = master_row[1] or ""
        valve_name = master_row[2] or ""
        valve_class = master_row[3] or ""
        material = master_row[4] or ""
        
        body_heat_no = master_row[7] or ""
        body_mpi_no = master_row[8] or ""
        body_rt_no = master_row[9] or ""
        connector_l_heat_no = master_row[10] or ""
        connector_l_mpi_no = master_row[11] or ""
        connector_l_rt_no = master_row[12] or ""
        connector_r_heat_no = master_row[13] or ""
        connector_r_mpi_no = master_row[14] or ""
        connector_r_rt_no = master_row[15] or ""
        

        all_pages_html = ""
        valid_tests = []

        for test_row in test_rows:
            test_id = test_row[0]
            test_name = test_row[1] or ""
            
            graph_image_base64 = get_graph_base64_for_test(excel_filepath, test_id, test_name)
            
            if graph_image_base64:
                valid_tests.append((test_row, graph_image_base64))

        if not valid_tests:
            return False
            
        total_pages = len(valid_tests)
        
        for idx, (test_row, graph_image_base64) in enumerate(valid_tests):
            test_id = test_row[0]
            test_name = test_row[1] or ""
            set_time = test_row[2] if test_row[2] is not None else ""
            set_pressure = test_row[3] if test_row[3] is not None else ""
            pressure_unit = test_row[4] or ""
            start_pressure = test_row[5] if test_row[5] is not None else ""
            end_pressure = test_row[6] if test_row[6] is not None else ""
            valve_status = test_row[7] or "UNKNOWN"
            if valve_status == "PASS":
                valve_status = "No leak observed"
            elif valve_status == "FAIL":
                valve_status = "Leak observed"
            else:
                valve_status = "UNKNOWN"
            
            logo_full_path = os.path.join(settings.BASE_DIR, 'standard_app', 'static', 'images', 'lnt-logo.png')
            try:
                with open(logo_full_path, 'rb') as img_f:
                    logo_path = "data:image/png;base64," + base64.b64encode(img_f.read()).decode('utf-8')
            except Exception:
                logo_path = ""
            
            context = {
                'test_type': test_name,
                'serial_no': valve_serial_no,
                'test_date': datetime.now(),
                'valve_name': valve_name,
                'tested_by': tested_by,
                'valve_size': valve_size,
                'valve_class': valve_class,
                'material': material,
                'body_heat_no': body_heat_no,
                'body_mpi_no': body_mpi_no,
                'connector_l_heat_no': connector_l_heat_no,
                'connector_l_mpi_no': connector_l_mpi_no,
                'connector_r_heat_no': connector_r_heat_no,
                'connector_r_mpi_no': connector_r_mpi_no,
                'set_pressure': set_pressure,
                'pressure_unit': pressure_unit,
                'duration': set_time,
                'start_pressure': start_pressure,
                'end_pressure': end_pressure,
                'work_order': "",
                'valve_status': valve_status,
                'chart_image_url': graph_image_base64,
                'page_number': idx + 1,
                'total_pages': total_pages,
                'logo_path': logo_path
            }
            
            page_html = render_to_string('graph_report_template.html', context)
            if idx < len(valid_tests) - 1:
                page_html = page_html.replace('</body>', '<div style="page-break-after: always;"></div></body>')
            
            all_pages_html += page_html

        # Generate PDF
        pdf_dir = "S:/Reports"
        os.makedirs(pdf_dir, exist_ok=True)
        filename = f"{valve_serial_no}_Count-{count_id}_report.pdf"
        filepath = os.path.join(pdf_dir, filename)
        
        HTML(string=all_pages_html).write_pdf(filepath)
        print(f"[PDF] Generated report: {filepath}")

        return True

    except Exception as e:
        print(f"[PDF] Error generating pdf report: {e}")
        import traceback
        traceback.print_exc()
        return None
