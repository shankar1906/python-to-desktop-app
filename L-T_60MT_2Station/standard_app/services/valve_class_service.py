from django.db import connection


def get_all_valve_classes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, VALVE_CLASS_ID, VALVE_CLASS_NAME, VALVE_CLASS_DESCRIPTION, VALVE_CLASS_STATUS
            FROM valveclass
            ORDER BY ID
        """)
        return cursor.fetchall()


def get_next_class_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COALESCE(MAX(VALVE_CLASS_ID), 0) + 1 FROM valveclass")
        return cursor.fetchone()[0]


def insert_valve_class(class_id, name, desc, status):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO valveclass (VALVE_CLASS_ID, VALVE_CLASS_NAME, VALVE_CLASS_DESCRIPTION, VALVE_CLASS_STATUS)
            VALUES (%s, %s, %s, %s)
        """, [class_id, name, desc, status])


def update_valve_class(class_id, new_class_id, name, desc, status):
    with connection.cursor() as cursor:
        # If class_id is being changed, update it along with other fields
        if class_id != new_class_id:
            cursor.execute("""
                UPDATE valveclass
                SET VALVE_CLASS_ID = %s, VALVE_CLASS_NAME = %s, VALVE_CLASS_DESCRIPTION = %s, VALVE_CLASS_STATUS = %s
                WHERE VALVE_CLASS_ID = %s
            """, [new_class_id, name, desc, status, class_id])
        else:
            cursor.execute("""
                UPDATE valveclass
                SET VALVE_CLASS_NAME = %s, VALVE_CLASS_DESCRIPTION = %s, VALVE_CLASS_STATUS = %s
                WHERE VALVE_CLASS_ID = %s
            """, [name, desc, status, class_id])


def delete_valve_class_record(class_id):
    with connection.cursor() as cursor:
        # Set VALVECLASS_ID to NULL in master_pressure_data first
        cursor.execute("""
            UPDATE master_pressure_data
            SET VALVE_CLASS_ID = NULL
            WHERE VALVE_CLASS_ID = %s
        """, [class_id])

        # Now delete from valveclass
        cursor.execute("DELETE FROM valveclass WHERE VALVE_CLASS_ID=%s", [class_id])
    
        


def check_duplicate_name(name, class_id=None):
    with connection.cursor() as cursor:
        if class_id:
            cursor.execute("SELECT 1 FROM valveclass WHERE LOWER(VALVE_CLASS_NAME)=LOWER(%s) AND VALVE_CLASS_ID!=%s", [name, class_id])
        else:
            cursor.execute("SELECT 1 FROM valveclass WHERE LOWER(VALVE_CLASS_NAME)=LOWER(%s)", [name])
        return cursor.fetchone()


def check_duplicate_class_id(class_id, exclude_class_id=None):
    with connection.cursor() as cursor:
        if exclude_class_id:
            cursor.execute("SELECT 1 FROM valveclass WHERE VALVE_CLASS_ID=%s AND VALVE_CLASS_ID!=%s", [class_id, exclude_class_id])
        else:
            cursor.execute("SELECT 1 FROM valveclass WHERE VALVE_CLASS_ID=%s", [class_id])
        return cursor.fetchone()


def delete_multiple_valve_classes(class_ids):
    if not class_ids:
        return 0

    placeholders = ",".join(["%s"] * len(class_ids))
    query = f"DELETE FROM valveclass WHERE VALVE_CLASS_ID IN ({placeholders})"

    with connection.cursor() as cursor:
        cursor.execute(query, class_ids)
    
    return cursor.rowcount