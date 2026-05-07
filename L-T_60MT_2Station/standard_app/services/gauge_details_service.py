from django.db import connection
from django.utils import timezone


def get_all_gauges():
    """Get all gauges from gauge_details table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT GD_ID, GD_SERIAL_NUMBER, GD_MEDIUM, 
                   GD_PRESSURE_RANGE_PSI, GD_PRESSURE_RANGE_BAR, `GD_PRESSURE_RANGE_KG/CM2`,
                   GD_DONE_DATE, GD_DUE_DATE, GD_STATION_ID, GD_STATUS
            FROM gauge_details
            ORDER BY GD_STATUS DESC, GD_ID
        """)
        return cursor.fetchall()


def get_next_gauge_id():
    """Get the next available GD_ID"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT COALESCE(MAX(GD_ID), 0) + 1 FROM gauge_details")
        result = cursor.fetchone()
        return int(result[0]) if result and result[0] is not None else 1


def insert_gauge(serial, medium, range_psi, range_bar, range_kgcm2, done_date, due_date, station_id, status):
    """Insert new gauge record"""
    now_ts = timezone.now()
    gd_id = get_next_gauge_id()
    
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO gauge_details (
                GD_ID, GD_SERIAL_NUMBER, GD_MEDIUM,
                GD_PRESSURE_RANGE_PSI, GD_PRESSURE_RANGE_BAR, `GD_PRESSURE_RANGE_KG/CM2`,
                GD_DONE_DATE, GD_DUE_DATE, GD_STATION_ID, GD_STATUS,
                GD_CREATED_DATE, GD_UPDATED_DATE
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, [gd_id, serial, medium, range_psi, range_bar, range_kgcm2,
              done_date, due_date, station_id, status, now_ts, now_ts])
    
    return gd_id


def update_gauge(gd_id, serial, medium, range_psi, range_bar, range_kgcm2, done_date, due_date, station_id, status):
    """Update existing gauge record"""
    now_ts = timezone.now()
    
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE gauge_details
            SET GD_SERIAL_NUMBER=%s, GD_MEDIUM=%s,
                GD_PRESSURE_RANGE_PSI=%s, GD_PRESSURE_RANGE_BAR=%s, `GD_PRESSURE_RANGE_KG/CM2`=%s,
                GD_DONE_DATE=%s, GD_DUE_DATE=%s, GD_STATION_ID=%s, GD_STATUS=%s,
                GD_UPDATED_DATE=%s
            WHERE GD_ID=%s
        """, [serial, medium, range_psi, range_bar, range_kgcm2,
              done_date, due_date, station_id, status, now_ts, gd_id])
    
    return cursor.rowcount


def delete_gauge_record(gd_id):
    """Delete gauge record by GD_ID"""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM gauge_details WHERE GD_ID=%s", [gd_id])
        return cursor.rowcount


def get_gauge_by_id(gd_id):
    """Get gauge by GD_ID"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT GD_ID, GD_SERIAL_NUMBER, GD_MEDIUM,
                   GD_PRESSURE_RANGE_PSI, GD_PRESSURE_RANGE_BAR, `GD_PRESSURE_RANGE_KG/CM2`,
                   GD_DONE_DATE, GD_DUE_DATE, GD_STATION_ID, GD_STATUS
            FROM gauge_details
            WHERE GD_ID=%s
        """, [gd_id])
        return cursor.fetchone()


def check_duplicate_serial(serial, exclude_gd_id=None):
    """Check if serial number already exists"""
    with connection.cursor() as cursor:
        if exclude_gd_id:
            cursor.execute("""
                SELECT COUNT(*) FROM gauge_details 
                WHERE GD_SERIAL_NUMBER=%s AND GD_ID != %s
            """, [serial, exclude_gd_id])
        else:
            cursor.execute("""
                SELECT COUNT(*) FROM gauge_details 
                WHERE GD_SERIAL_NUMBER=%s
            """, [serial])
        return cursor.fetchone()[0] > 0


def count_enabled_gauges_by_station(station_id, exclude_gd_id=None):
    """Count enabled gauges for a specific station"""
    with connection.cursor() as cursor:
        if exclude_gd_id:
            cursor.execute("""
                SELECT COUNT(*) FROM gauge_details 
                WHERE GD_STATION_ID=%s AND GD_STATUS=1 AND GD_ID != %s
            """, [station_id, exclude_gd_id])
        else:
            cursor.execute("""
                SELECT COUNT(*) FROM gauge_details 
                WHERE GD_STATION_ID=%s AND GD_STATUS=1
            """, [station_id])
        return cursor.fetchone()[0]
