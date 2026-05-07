from urllib import request
from django.db import connection
from django.shortcuts import redirect
from django.contrib import messages

def getall_testtype():
     with connection.cursor() as cursor:
            cursor.execute("""
                SELECT tt.TEST_TYPE_ID, tt.TEST_TYPE_NAME, tt.TEST_CATEGORY_ID, c.TEST_CATEGORY_NAME, tt.TEST_STATUS
                FROM test_type tt
                LEFT JOIN category c ON tt.TEST_CATEGORY_ID = c.TEST_CATEGORY_ID
                ORDER BY tt.TEST_STATUS DESC, tt.TEST_TYPE_ID
            """)
            return cursor.fetchall()
        
def get_enabled_categories():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT TEST_CATEGORY_ID, TEST_CATEGORY_NAME
            FROM category
            WHERE CATEGORY_STATUS = 'ENABLE'
            ORDER BY TEST_CATEGORY_NAME
        """)
        return cursor.fetchall()
    
def check_duplicate_testname(testname_lower, test_type_id):
    with connection.cursor() as cursor:
        # Check for duplicates in database (case-insensitive)
        cursor.execute("""
            SELECT TEST_TYPE_ID, TEST_TYPE_NAME
            FROM test_type
            WHERE LOWER(TEST_TYPE_NAME) = %s AND TEST_TYPE_ID != %s
        """, [testname_lower, test_type_id])
        return cursor.fetchone()
    
def update_testtype(testname, category_id, status, test_type_id):
    with connection.cursor() as cursor:
        cursor.execute(
                    """
                    UPDATE test_type
                    SET TEST_TYPE_NAME = %s,
                        TEST_CATEGORY_ID = %s,
                        TEST_STATUS = %s,
                        updated_at = NOW()
                    WHERE TEST_TYPE_ID = %s
                """,
                    [
                        testname,
                        category_id,
                        status,
                        test_type_id
                    ],
                )
        return cursor.rowcount