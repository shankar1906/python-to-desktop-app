from django.db import connection

def check_duplicate_category(category_id, testname):
   
    testname_lower = testname.strip().lower()

    with connection.cursor() as cursor:  
        # Check for duplicates in database (case-insensitive)
            cursor.execute("""
                SELECT TEST_CATEGORY_ID, TEST_CATEGORY_NAME
                FROM category
                WHERE LOWER(TEST_CATEGORY_NAME) = %s AND TEST_CATEGORY_ID != %s
            """, [testname_lower, category_id])

            duplicate = cursor.fetchone()

    return duplicate is not None


def update_category(category_ids, testnames, mediums, statuses):
    
    with connection.cursor() as cursor:
                for category_id, testname, medium, status in zip(category_ids, testnames, mediums, statuses):
                    category_id = int(category_id)  # Convert to int
                    
                    # Convert empty string to None for database NULL
                    medium_value = medium if medium and medium.strip() else None
                    
                    cursor.execute("""
                        UPDATE category
                        SET TEST_CATEGORY_NAME = %s,
                            TEST_CATEGORY_MEDIUM = %s,
                            CATEGORY_STATUS = %s,
                            UPDATED_DATE = NOW()
                        WHERE TEST_CATEGORY_ID = %s
                    """, [testname, medium_value, status, category_id])