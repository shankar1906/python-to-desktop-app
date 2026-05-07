from django.db import connection


def distinct_valve_serial_numbers_from_pressure_analysis():
    """Distinct non-empty valve serials present in pressure_analysis (for Graph / VTR dropdowns)."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT DISTINCT TRIM(VALVE_SER_NO) AS ser
            FROM pressure_analysis
            WHERE VALVE_SER_NO IS NOT NULL
              AND TRIM(VALVE_SER_NO) <> ''
            ORDER BY ser
            """
        )
        rows = cursor.fetchall()
    return [row[0] for row in rows if row and row[0] is not None]


def latest_count_id_for_valve(valve_serial_no):
    """Latest COUNT_ID in pressure_analysis for this serial (for VTR / graph reports)."""
    if not valve_serial_no or not str(valve_serial_no).strip():
        return None
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT MAX(COUNT_ID)
            FROM pressure_analysis
            WHERE VALVE_SER_NO = %s
            """,
            [str(valve_serial_no).strip()],
        )
        row = cursor.fetchone()
    if not row or row[0] is None:
        return None
    return row[0]


def master_temp_data_id_for_valve(valve_serial_no):
    """
    master_temp_data.ID used as station_id for generate_excel_report (gauge mapping),
    matching cycle_complete_service behaviour.
    """
    if not valve_serial_no or not str(valve_serial_no).strip():
        return 1
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT ID FROM master_temp_data
            WHERE VALVE_SER_NO = %s
            ORDER BY ID
            LIMIT 1
            """,
            [str(valve_serial_no).strip()],
        )
        row = cursor.fetchone()
    return int(row[0]) if row and row[0] is not None else 1
