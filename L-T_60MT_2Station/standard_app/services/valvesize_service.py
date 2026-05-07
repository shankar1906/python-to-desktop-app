from django.db import connection, transaction


def get_all_valvesize():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ID, VALVE_SIZE_ID, VALVE_SIZE_NAME, VALVE_SIZE_DESCRIPTION, PART_NO, PART_NAME, VALVE_SIZE_STATUS
            FROM valvesize
            ORDER BY VALVE_SIZE_ID
        """)
       
        return cursor.fetchall()
    

def get_all_valvetype():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT VALVE_TYPE_ID, VALVE_TYPE_NAME
            FROM valve_type
            ORDER BY VALVE_TYPE_ID
        """)

        return cursor.fetchall()
    

def get_enabled_categories():

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TEST_CATEGORY_NAME, DURATION_COLUMN_NAME
            FROM category
            WHERE CATEGORY_STATUS='ENABLE'
            ORDER BY TEST_CATEGORY_ID
        """)
        
        return cursor.fetchall()

def delete_multiple_valvesize(size_ids):
    if not size_ids:
        return 0

    placeholders = ",".join(["%s"] * len(size_ids))
    
    with transaction.atomic():
        with connection.cursor() as cursor:
            # Delete related duration data
            cursor.execute(f"DELETE FROM master_duration_data WHERE VALVE_SIZE_ID IN ({placeholders})", size_ids)
            
            # Delete related degree data
            cursor.execute(f"DELETE FROM master_degree_data WHERE VALVE_SIZE_ID IN ({placeholders})", size_ids)
            
            # Delete the valve size itself
            cursor.execute(f"DELETE FROM valvesize WHERE VALVE_SIZE_ID IN ({placeholders})", size_ids)
            
            return cursor.rowcount

    

# def get_all_valvesize():

