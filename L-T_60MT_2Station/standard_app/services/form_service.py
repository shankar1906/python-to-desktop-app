from django.db import connection
from standard_app.views.api.configuration_api_views import TestleadSmartsyncx
from standard_app.src import HmiAddress


def get_valve_standard():
    with connection.cursor() as cursor:
        cursor.execute("SELECT STANDARD_NAME FROM standard WHERE STANDARD_STATUS=%s", ['Enabled'])
        return [row[0] for row in cursor.fetchall()]
    
def get_valve_size():
    with connection.cursor() as cursor:
        cursor.execute("SELECT VALVE_SIZE_NAME FROM valvesize WHERE VALVE_SIZE_STATUS=%s", ['Enabled'])
        return [row[0] for row in cursor.fetchall()]

def get_valve_class():
    with connection.cursor() as cursor:
        cursor.execute("SELECT VALVE_CLASS_NAME FROM valveclass WHERE VALVE_CLASS_STATUS=%s", ['Enabled'])
        return [row[0] for row in cursor.fetchall()]

def get_shell_material():
    with connection.cursor() as cursor:
        cursor.execute("SELECT SHELL_MATERIAL_NAME FROM shell_material WHERE SHELL_MATERIAL_STATUS=%s", ['Enabled'])
        return [row[0] for row in cursor.fetchall()]
    
def get_valve_type():
    with connection.cursor() as cursor:
        cursor.execute("SELECT VALVE_TYPE_NAME FROM valve_type WHERE VALVE_TYPE_STATUS=%s", ['Enabled'])
        return [row[0] for row in cursor.fetchall()]
    
def get_testername():
    """Get all employee names (kept for backward compatibility)"""
    with connection.cursor() as cursor:
        cursor.execute("select name from employee where superuser=%s",[0])
        return [row[0] for row in cursor.fetchall()]

def get_assemblers():
    """Get employees with type 'Approver' for Assembled By dropdown"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM employee WHERE superuser=%s AND LOWER(employee_type)=%s ORDER BY name", [0, 'approver'])
        return [row[0] for row in cursor.fetchall()]

def get_testers():
    """Get employees with type 'Tester' for Tested By dropdown"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM employee WHERE superuser=%s AND LOWER(employee_type)=%s ORDER BY name", [0, 'tester'])
        return [row[0] for row in cursor.fetchall()]


def get_testname(standard, valve_size, valve_type, shell_material, valve_class):
    with connection.cursor() as cursor:
        
        # Get standard_id
        cursor.execute("SELECT STANDARD_ID FROM standard WHERE STANDARD_NAME=%s", [standard])
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Standard '{standard}' not found in database.")
        standard_id = result[0]

        # Get size_id
        cursor.execute("SELECT VALVE_SIZE_ID FROM valvesize WHERE VALVE_SIZE_NAME=%s", [valve_size])
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Valve Size '{valve_size}' not found in database.")
        size_id = result[0]

        # Get type_id
        cursor.execute("SELECT VALVE_TYPE_ID FROM valve_type WHERE VALVE_TYPE_NAME=%s", [valve_type])
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Valve Type '{valve_type}' not found in database.")
        type_id = result[0]

        # Get test_ids for this valve type
        cursor.execute("SELECT TEST_TYPE_ID FROM valvetype_testtype WHERE VALVE_TYPE_ID=%s", [type_id])
        test_ids = cursor.fetchall()
        if not test_ids:
            raise ValueError(f"No tests found for Valve Type '{valve_type}'. Please configure tests for this valve type.")

        # Get shell_material_id
        cursor.execute("SELECT SHELL_MATERIAL_ID FROM shell_material WHERE SHELL_MATERIAL_NAME=%s", [shell_material])
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Body Material '{shell_material}' not found in database.")
        shell_material_id = result[0]

        # Get class_id
        cursor.execute("SELECT VALVE_CLASS_ID FROM valveclass WHERE VALVE_CLASS_NAME=%s", [valve_class])
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Valve Class '{valve_class}' not found in database.")
        class_id = result[0]

        # Get degree data
        cursor.execute("SELECT OPEN_DEGREE, CLOSE_DEGREE FROM master_degree_data WHERE VALVE_SIZE_ID=%s AND TYPE_ID=%s", [size_id, type_id])
        degree = cursor.fetchone()
        # if not degree:
        #     raise ValueError(f"Degree data not found for combination: Size ID={size_id} ('{valve_size}') and Type ID={type_id} ('{valve_type}'). Please add this combination to master_degree_data table.")
        
        # Check for null values in degree
        # if degree[0] is None or degree[1] is None:
        #     raise ValueError(f"Degree data contains NULL values for Size '{valve_size}' and Type '{valve_type}'.")
        
        # Get test names
        test_name = []
        for t in test_ids:
            cursor.execute("SELECT TEST_TYPE_NAME FROM test_type WHERE TEST_TYPE_ID=%s", [t[0]])
            result = cursor.fetchone()
            if result:
                test_name.append(result[0])
            else:
                raise ValueError(f"Test type with ID {t[0]} not found in test_type table.")

        # Get pressure and duration columns
        pressure = []
        duration = []

        for t in test_ids:
            # Get pressure column name and medium from category table via test_type
            cursor.execute("""
                SELECT c.PRESSURE_COLUMN_NAME, c.TEST_CATEGORY_MEDIUM, c.DURATION_COLUMN_NAME
                FROM test_type tt
                JOIN category c ON tt.TEST_CATEGORY_ID = c.TEST_CATEGORY_ID
                WHERE tt.TEST_TYPE_ID=%s
            """, [t[0]])
            result = cursor.fetchone()
            
            if not result:
                raise ValueError(f"Category data not found for test ID {t[0]}.")
            
            pre_col, medium, dur_col = result
            
            if not pre_col:
                raise ValueError(f"Pressure column name is NULL for test ID {t[0]}.")
            
            query = f"SELECT {pre_col} FROM master_pressure_data WHERE SHELL_MATERIAL_ID=%s AND VALVE_CLASS_ID=%s"
            cursor.execute(query, [shell_material_id, class_id])
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Pressure data not found for combination: Body Material '{shell_material}' and Class '{valve_class}'. Please add this combination to master_pressure_data table.")
            
            pressure_value = row[0]
            if pressure_value is None:
                raise ValueError(f"Pressure value is NULL for Body Material '{shell_material}' and Class '{valve_class}' in column '{pre_col}'.")
            pressure.append(pressure_value)

            # Get duration using the dur_col from the same query
            if not dur_col:
                raise ValueError(f"Duration column name is NULL for test ID {t[0]}.")
            
            print(f"size_id: {size_id}, standard_id: {standard_id} << ")
            query = f"SELECT {dur_col} FROM master_duration_data WHERE VALVE_SIZE_ID=%s AND `STANDARD`=%s "
            cursor.execute(query, [size_id, standard_id])
            row1 = cursor.fetchone()
            if not row1:
                raise ValueError(f"Duration data not found for combination: Size '{valve_size}' and Standard '{standard}'")
            
            duration_value = row1[0]
            if duration_value is None:
                raise ValueError(f"Duration value is NULL for Size '{valve_size}' and Standard '{standard}' in column '{dur_col}'.")
            duration.append(duration_value)

        return test_name, pressure, duration, test_ids,degree


# ==================== STATION SERVICES ====================

def get_status():
    """Get status for both stations and sync status"""
    with connection.cursor() as cursor:
        # Fetch statuses
        cursor.execute("SELECT STATION_STATUS FROM master_temp_data WHERE id=1")
        station1_status = cursor.fetchone()[0]

        cursor.execute("SELECT STATION_STATUS FROM master_temp_data WHERE id=2")
        station2_status = cursor.fetchone()[0]
        
        # Always use Sync Mode (no longer reading from HMI)
        sync_status = 1  # 1 = Sync Mode
        
        print("sync_status (always Sync Mode):", sync_status)
        
        return station1_status, station2_status, sync_status

def get_station_data():
    """Get data for both stations"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT VALVE_CLASS_NAME, VALVE_SIZE_NAME, SHELL_MATERIAL_NAME, VALVE_TYPE_NAME, PRESSURE_UNIT 
            FROM master_temp_data WHERE id=1
        """)
        station1_data = cursor.fetchone()

        cursor.execute("""
            SELECT VALVE_CLASS_NAME, VALVE_SIZE_NAME, SHELL_MATERIAL_NAME, VALVE_TYPE_NAME, PRESSURE_UNIT 
            FROM master_temp_data WHERE id=2
        """)
        station2_data = cursor.fetchone()
        
        return station1_data, station2_data

def compare_station_data(station1_data, station2_data):
    """Compare data between two stations"""
    return station1_data == station2_data

def cancel_station1():
    with connection.cursor() as cursor:
        # Delete common test data (where VALVE_SERIAL_NO IS NULL)
        # cursor.execute("DELETE FROM temp_testing_data WHERE VALVE_SERIAL_NO IS NULL")
        cursor.execute("TRUNCATE TABLE temp_testing_data")
        cursor.execute("UPDATE master_temp_data SET STATION_STATUS=%s, CYCLE_COMPLETE=%s WHERE ID=%s", ["Disabled", "No", 1])

        cols = []
        for i in range(1, 51):
            cols.append(f"COL{i}_NAME=''")
            cols.append(f"COL{i}_VALUE=''")
        set_clause = ", ".join(cols)
        
        cursor.execute(f"UPDATE master_temp_data SET {set_clause} WHERE ID=1")
        connection.commit()
        
def cancel_station2():
    with connection.cursor() as cursor:
        # Delete common test data (where VALVE_SERIAL_NO IS NULL)
        # cursor.execute("DELETE FROM temp_testing_data WHERE VALVE_SERIAL_NO IS NULL")
        cursor.execute("TRUNCATE TABLE temp_testing_data")
        cursor.execute("UPDATE master_temp_data SET STATION_STATUS=%s, CYCLE_COMPLETE=%s WHERE ID=%s", ["Disabled", "No", 2])

        cols = []
        for i in range(1, 51):
            cols.append(f"COL{i}_NAME=''")
            cols.append(f"COL{i}_VALUE=''")
        set_clause = ", ".join(cols)
        
        cursor.execute(f"UPDATE master_temp_data SET {set_clause} WHERE ID=2")
        connection.commit()

def clear_station1():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM temp_testing_data WHERE VALVE_SERIAL_NO IS NULL")
        cursor.execute("UPDATE master_temp_data SET STATION_STATUS=%s, CYCLE_COMPLETE=%s WHERE ID=%s", ["Disabled", "No", 1])

        cols = []
        for i in range(1, 51):
            cols.append(f"COL{i}_NAME=''")
            cols.append(f"COL{i}_VALUE=''")
        set_clause = ", ".join(cols)

        cursor.execute(f"UPDATE master_temp_data SET {set_clause} WHERE ID=1")
        connection.commit()
    
def clear_station2():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM temp_testing_data WHERE VALVE_SERIAL_NO IS NULL")
        cursor.execute("UPDATE master_temp_data SET STATION_STATUS=%s, CYCLE_COMPLETE=%s WHERE ID=%s", ["Disabled", "No", 2])

        cols = []
        for i in range(1, 51):
            cols.append(f"COL{i}_NAME=''")
            cols.append(f"COL{i}_VALUE=''")
        set_clause = ", ".join(cols)

        cursor.execute(f"UPDATE master_temp_data SET {set_clause} WHERE ID=2")
        connection.commit()

