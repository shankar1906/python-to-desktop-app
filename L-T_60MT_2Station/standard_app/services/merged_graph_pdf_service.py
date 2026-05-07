"""
Build merged multi-page graph PDF (merged_report.html) from station export Excel + pressure_analysis.
"""
import base64
import os
from datetime import datetime

from django.db import connection
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML

from standard_app.services.pressure_analysis_serial_service import latest_count_id_for_valve

EXPORT_EXCEL_DIR = "D:/LandT-10MT-KPM_DB_export"


def _report_base_path():
    default_path = "D:/LandT-10MT-KPM_DB_export/Reports"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT REPORT_PATH FROM configuration_table LIMIT 1")
            row = cursor.fetchone()
        if row and row[0] and str(row[0]).strip():
            p = str(row[0]).strip()
            drive = os.path.splitdrive(p)[0]
            if drive and not os.path.exists(drive + os.sep):
                return default_path
            return p
    except Exception:
        pass
    return default_path


def _logo_base64():
    try:
        logo_path = os.path.join(settings.BASE_DIR, "standard_app", "static", "images", "braylogo.webp")
        with open(logo_path, "rb") as image_file:
            return f"data:image/webp;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
    except Exception:
        return ""


def build_merged_graph_pdf(valve_serial_no: str):
    """
    Latest COUNT_ID for serial; reads ``{serial}_Count-{count}.xlsx`` from EXPORT_EXCEL_DIR.
    Returns dict: ok, path (pdf filepath), error (message if failed).
    """
    valve_serial_no = (valve_serial_no or "").strip()
    if not valve_serial_no:
        return {"ok": False, "path": None, "error": "Serial number is required."}

    count_id = latest_count_id_for_valve(valve_serial_no)
    if count_id is None:
        return {"ok": False, "path": None, "error": "No pressure_analysis data for this serial."}

    excel_filename = f"{valve_serial_no}_Count-{count_id}.xlsx"
    excel_filepath = os.path.join(EXPORT_EXCEL_DIR, excel_filename)
    if not os.path.isfile(excel_filepath):
        return {
            "ok": False,
            "path": None,
            "error": (
                f"Export Excel not found ({excel_filepath}). "
                "This file is created when the test cycle completes and exports station data."
            ),
        }

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT VALVE_SER_NO, VALVESIZE_NAME, COL4_VALUE, COL7_VALUE, COL8_VALUE
            FROM pressure_analysis
            WHERE VALVE_SER_NO = %s AND COUNT_ID = %s
            LIMIT 1
            """,
            [valve_serial_no, count_id],
        )
        master_row = cursor.fetchone()
        if not master_row:
            return {"ok": False, "path": None, "error": "No pressure_analysis row for this serial and count."}

        cursor.execute(
            """
            SELECT TEST_ID, TEST_NAME, SET_TIME, SET_PRESSURE,
                   PRESSURE_UNIT, START, END, VALVE_STATUS
            FROM pressure_analysis
            WHERE VALVE_SER_NO = %s AND COUNT_ID = %s
            ORDER BY TEST_ID ASC
            """,
            [valve_serial_no, count_id],
        )
        test_rows = cursor.fetchall()

    if not test_rows:
        return {"ok": False, "path": None, "error": "No tests in pressure_analysis for this serial and count."}

    from standard_app.views.api.generate_report_views import graph_generation_from_excel

    logo_base64 = _logo_base64()
    serial_no = master_row[0] or ""
    valve_size = master_row[1] or ""
    part_no = master_row[2] or ""
    tested_by = master_row[4] or ""
    current_date = datetime.now().strftime("%d-%m-%Y")

    valid_tests = []
    for test_row in test_rows:
        test_id = test_row[0]
        test_type = test_row[1] or ""
        graph_image_base64 = graph_generation_from_excel(excel_filepath, test_id, test_type)
        if graph_image_base64 is not None:
            valid_tests.append((test_row, graph_image_base64))

    if not valid_tests:
        return {
            "ok": False,
            "path": None,
            "error": "No graphs could be built from the export Excel for this cycle.",
        }

    all_pages_html = ""
    for idx, (test_row, graph_image_base64) in enumerate(valid_tests):
        test_id = test_row[0]
        test_type = test_row[1] or ""
        set_time = test_row[2] if test_row[2] else "0"
        set_pressure = test_row[3] if test_row[3] else "0"
        pressure_unit = test_row[4] if test_row[4] else "bar"
        start_time_raw = test_row[5]
        end_time_raw = test_row[6]
        valve_status = test_row[7] if test_row[7] else "UNKNOWN"

        start_time = ""
        end_time = ""
        if start_time_raw:
            if isinstance(start_time_raw, str):
                start_time = start_time_raw
            else:
                start_time = start_time_raw.strftime("%H:%M:%S")
        if end_time_raw:
            if isinstance(end_time_raw, str):
                end_time = end_time_raw
            else:
                end_time = end_time_raw.strftime("%H:%M:%S")

        time_diff = ""
        if start_time and end_time:
            try:
                start_dt = datetime.strptime(start_time, "%H:%M:%S")
                end_dt = datetime.strptime(end_time, "%H:%M:%S")
                time_diff = str(end_dt - start_dt)
            except Exception:
                time_diff = "N/A"

        context = {
            "serial_no": serial_no,
            "valve_size": valve_size,
            "part_no": part_no,
            "tested_by": tested_by,
            "test_date": current_date,
            "test_type": test_type,
            "set_time": set_time,
            "set_pressure": set_pressure,
            "pressure_unit": pressure_unit,
            "start_time": start_time,
            "end_time": end_time,
            "time_diff": time_diff,
            "valve_status": valve_status,
            "current_date": current_date,
            "graph_image_base64": graph_image_base64,
            "logo_base64": logo_base64,
        }

        page_html = render_to_string("merged_report.html", context)
        if idx < len(valid_tests) - 1:
            page_html = page_html.replace(
                "</body>",
                '<div style="page-break-after: always;"></div></body>',
            )
        all_pages_html += page_html

    base_report_path = _report_base_path()
    pdf_folder_path = os.path.join(base_report_path, "pdf")
    os.makedirs(pdf_folder_path, exist_ok=True)

    out_name = f"{valve_serial_no}_Count-{count_id}_merged_graph_report.pdf"
    filepath = os.path.join(pdf_folder_path, out_name)

    try:
        HTML(string=all_pages_html).write_pdf(filepath)
    except Exception as e:
        return {"ok": False, "path": None, "error": f"PDF generation failed: {e}"}

    return {"ok": True, "path": filepath, "error": None}
