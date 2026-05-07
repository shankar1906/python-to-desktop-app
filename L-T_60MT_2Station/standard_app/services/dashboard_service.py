from django.db import connection

def check_incomplete_test():
    with connection.cursor() as cursor:
        cursor.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS  = %s", ['Enabled'])
        rows = cursor.fetchall()
        if rows:
            results = []
            for valve_ser_no in rows:
                results.append({
                    "valve_ser_no": valve_ser_no[0]
                })
            return results
        else:
            return None
    
def delete_test(valve_ser_no):
    """
    Delete test data for given valve serial number(s).
    If valve_ser_no is a single value, it deletes that one.
    This function also disables ALL enabled stations in master_temp_data.
    """
    with connection.cursor() as cursor:
        # Get all enabled stations to delete their test data
        cursor.execute("SELECT VALVE_SER_NO FROM master_temp_data WHERE STATION_STATUS = 'Enabled'")
        enabled_stations = cursor.fetchall()
        enabled_valve_ser_nos = [row[0] for row in enabled_stations]
        
        if not enabled_valve_ser_nos:
            # No enabled stations, nothing to delete
            connection.commit()
            return True
        
        # Delete test data for ALL enabled stations
        for vsn in enabled_valve_ser_nos:
            cursor.execute("SELECT TEST_ID, COUNT_ID FROM temp_pressure_analysis WHERE VALVE_SER_NO = %s", [vsn])
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    test_id, count_id = row
                    cursor.execute(
                        "DELETE FROM pressure_analysis WHERE VALVE_SER_NO = %s AND TEST_ID = %s AND COUNT_ID = %s",
                        [vsn, test_id, count_id]
                    )
        
        # Truncate all current status tables
        cursor.execute("TRUNCATE TABLE current_status_station1")
        cursor.execute("TRUNCATE TABLE current_status_station2")
        cursor.execute("TRUNCATE TABLE temp_testing_data")
        cursor.execute("TRUNCATE TABLE temp_pressure_analysis")
        
        # Disable all enabled stations in master_temp_data
        cursor.execute("UPDATE master_temp_data SET STATION_STATUS = 'Disabled', CYCLE_COMPLETE = 'No' WHERE STATION_STATUS = 'Enabled'")
        
    connection.commit()
    return True
    
