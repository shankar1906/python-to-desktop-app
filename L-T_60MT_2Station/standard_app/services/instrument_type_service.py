from django.db import connection


def get_all_instrument_types():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT INSTRUMENT_ID, INSTRUMENT_TYPE, INSTRUMENT_SERIAL_NUMBER, INSTRUMENT_DONE_DATE, INSTRUMENT_DUE_DATE, INSTRUMENT_DUE_ALARM, INSTRUMENT_STATUS
            FROM instrument_categories
            ORDER BY INSTRUMENT_STATUS DESC, INSTRUMENT_ID
        """)
        return cursor.fetchall()


def get_next_instrument_type_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COALESCE(MAX(INSTRUMENT_ID), 0) + 1 FROM instrument_categories")
        return cursor.fetchone()[0]


def insert_instrument_type(type_id, name, serial_no, done_date, due_date, status):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO instrument_categories
            (INSTRUMENT_ID, INSTRUMENT_TYPE, INSTRUMENT_SERIAL_NUMBER, INSTRUMENT_DONE_DATE, INSTRUMENT_DUE_DATE, INSTRUMENT_DUE_ALARM, INSTRUMENT_STATUS, CREATED_DATE, UPDATED_DATE)
            VALUES (%s, %s, %s, %s, %s, CASE WHEN %s < CURDATE() THEN 1 ELSE 0 END, %s, NOW(), NOW())
        """, [type_id, name, serial_no, done_date, due_date, due_date, status])


def update_instrument_type(type_id, name, serial_no, done_date, due_date, status):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE instrument_categories
            SET INSTRUMENT_TYPE = %s, INSTRUMENT_SERIAL_NUMBER = %s, INSTRUMENT_DONE_DATE = %s, INSTRUMENT_DUE_DATE = %s, 
                INSTRUMENT_DUE_ALARM = CASE WHEN %s < CURDATE() THEN 1 ELSE 0 END,
                INSTRUMENT_STATUS = %s, UPDATED_DATE = NOW()
            WHERE INSTRUMENT_ID = %s
        """, [name, serial_no, done_date, due_date, due_date, status, type_id])


def delete_instrument_type_record(type_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM instrument_categories WHERE INSTRUMENT_ID=%s", [type_id])


def check_duplicate_name(name, exclude_id=None):
    with connection.cursor() as cursor:
        if exclude_id and str(exclude_id).strip():
            cursor.execute(
                "SELECT INSTRUMENT_ID FROM instrument_categories WHERE LOWER(INSTRUMENT_TYPE)=LOWER(%s) AND INSTRUMENT_ID != %s",
                [name, exclude_id]
            )
        else:
            cursor.execute(
                "SELECT INSTRUMENT_ID FROM instrument_categories WHERE LOWER(INSTRUMENT_TYPE)=LOWER(%s)",
                [name]
            )
        return cursor.fetchone()


def check_duplicate_serial_no(serial_no, exclude_id=None):
    with connection.cursor() as cursor:
        if exclude_id and str(exclude_id).strip():
            cursor.execute(
                "SELECT INSTRUMENT_ID FROM instrument_categories WHERE LOWER(INSTRUMENT_SERIAL_NUMBER)=LOWER(%s) AND INSTRUMENT_ID != %s",
                [serial_no, exclude_id]
            )
        else:
            cursor.execute(
                "SELECT INSTRUMENT_ID FROM instrument_categories WHERE LOWER(INSTRUMENT_SERIAL_NUMBER)=LOWER(%s)",
                [serial_no]
            )
        return cursor.fetchone()




def update_instrument_due_alarms():
    """Update INSTRUMENT_DUE_ALARM flag: 1 if passed, 0 if future/today"""
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE instrument_categories 
            SET INSTRUMENT_DUE_ALARM = CASE 
                WHEN INSTRUMENT_DUE_DATE < CURDATE() THEN 1 
                ELSE 0 
            END
            WHERE INSTRUMENT_DUE_DATE IS NOT NULL
        """)

