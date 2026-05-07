from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
from standard_app.services.save_station1_service import (
    save_station,
    check_duplicate_serial_station1, check_duplicate_serial_station2,
    check_hmi_connection
)
from standard_app.views.api.configuration_api_views import TestleadSmartsyncx
from standard_app.src import HmiAddress
from django.db import connection


def write_to_hmi(place, value):
    try:
        TestleadSmartsyncx.write_register(place, value)
        return True
    except Exception as e:
        print(f"[Error writing to HMI] {e}")
        isconnected = False
        return False

def map_dynamic_columns(field_dict, skip_keys):
    def get_explicit_col(key):
        # Extremely robust normalization: replace all non-alphanumeric with underscore, then strip
        ku = re.sub(r'[^A-Z0-9]', '_', key.upper()).strip('_')
        # Also handle cases where double underscores might be created
        while '__' in ku:
            ku = ku.replace('__', '_')
            
        if "HEAT_NO" in ku or "HT_NO" in ku:
            if "BODY" in ku: return 9
            if ("BONNET" in ku or "CONNECTOR_L" in ku) and "EXTN" not in ku and "CONNECTOR_R" not in ku: return 12
            if "EXTN" in ku or "CONNECTOR_R" in ku: return 15
        if "MPI" in ku or "DP_NO" in ku:
            if "BODY" in ku: return 10
            if ("BONNET" in ku or "CONNECTOR_L" in ku) and "EXTN" not in ku and "CONNECTOR_R" not in ku: return 13
            if "EXTN" in ku or "CONNECTOR_R" in ku: return 16
        if "RT_NO" in ku:
            if "BODY" in ku: return 11
            if ("BONNET" in ku or "CONNECTOR_L" in ku) and "EXTN" not in ku and "CONNECTOR_R" not in ku: return 14
            if "EXTN" in ku or "CONNECTOR_R" in ku: return 17
        return None

    explicit_col_names = {
        9: "BODY_HEAT_NO", 10: "BODY_MPI_DP_NO", 11: "BODY_RT_NO",
        12: "CONNECTOR_L_HEAT_NO", 13: "CONNECTOR_L_MPI_DP_NO", 14: "CONNECTOR_L_RT_NO",
        15: "CONNECTOR_R_HEAT_NO", 16: "CONNECTOR_R_MPI_DP_NO", 17: "CONNECTOR_R_RT_NO"
    }
    explicit_data = {i: "" for i in range(9, 18)}

    normal_fields = {}
    for key, value in field_dict.items():
        if key in skip_keys:
            continue
        
        col_num = get_explicit_col(key)
        if col_num:
            explicit_data[col_num] = value
        else:
            normal_fields[key] = value

    update_fields = []
    update_values = []
    
    index = 1
    for key, value in normal_fields.items():
        if 9 <= index <= 17:
            index = 18
            
        if index > 50:
            break
            
        update_fields.append(f"COL{index}_NAME = %s")
        update_fields.append(f"COL{index}_VALUE = %s")
        update_values.extend([key, value])
        index += 1
        if 9 <= index <= 17:
            index = 18

    for col_num in range(9, 18):
        update_fields.append(f"COL{col_num}_NAME = %s")
        update_fields.append(f"COL{col_num}_VALUE = %s")
        update_values.extend([explicit_col_names[col_num], explicit_data[col_num]])
        
    return update_fields, update_values

@csrf_exempt
def save_station1_form(request):
    print("[save_station1_form] Function called")
    if request.method != "POST":
        print("[save_station1_form] ERROR: Not a POST request")
        return JsonResponse({"error": "POST method required"}, status=400)

    try:
        print("[save_station1_form] Checking HMI connection...")
        # Check HMI connection status before saving
        hmi_connected = check_hmi_connection()
        if not hmi_connected:
            print("[save_station1_form] WARNING: HMI not connected - proceeding anyway")
            # Continue with save even if HMI is not connected
            # return JsonResponse({
            #     "status": "error",
            #     "message": "HMI is not connected. Please connect HMI before saving the form."
            # }, status=400)
        
        print("[save_station1_form] HMI connected, parsing request data...")
        data = json.loads(request.body.decode("utf-8"))
        print(f"[save_station1_form] Received data keys: {data.keys()}")
    
        fields = data.get("fields", [])
        print(f"[save_station1_form] Number of fields: {len(fields)}")
        field_dict = {item.get("name"): item.get("value") for item in fields}
        pressureunit = field_dict.get("pressureunit_s1")
        
        # Check if both stations have the same serial number
        station1_serial = field_dict.get("VALVE_SER_NO")
        print(f"[save_station1_form] Station 1 serial: {station1_serial}")
        is_duplicate, duplicate_station_id = check_duplicate_serial_station1(station1_serial)
        
        if is_duplicate:
            print(f"[save_station1_form] ERROR: Duplicate serial number: {station1_serial}")
            return JsonResponse({
                "status": "error",
                "message": f"Duplicate serial number detected! Serial number '{station1_serial}' is already used in Station {duplicate_station_id}. Please use a different serial number."
            }, status=400)
        
        station_status = "Enabled"
        cycle_complete = "No"
        testname = data.get("testname")
        test_pressure = data.get("test_pressure")
        test_duration = data.get("test_duration")
        active_testid = data.get("test_id")
        diabled_testid = data.get("diabled_testid")
        open_degree_s1 = data.get("open_degree_s1")
        close_degree_s1 = data.get("close_degree_s1")
        # Always use Sync mode (removed test_mode parameter)
        test_mode = "Sync"
        
        print(f"[save_station1_form] Degree values - Open: {open_degree_s1}, Close: {close_degree_s1}")
        print(f"[save_station1_form] Active tests: {len(active_testid) if active_testid else 0}")
        
        # Validate degree values
        # if open_degree_s1 is None or close_degree_s1 is None:
        #     print("[save_station1_form] ERROR: Degree values missing")
        #     return JsonResponse({
        #         "status": "error",
        #         "message": "Set open degree and close degree values are required but not received."
        #     }, status=400)
        
        # Check if at least one test is active (enabled)
        if not active_testid or len(active_testid) == 0:
            print("[save_station1_form] ERROR: No active tests")
            return JsonResponse({
                "status": "error",
                "message": "Please enable at least one test to proceed. Cannot save form without any active tests."
            }, status=400)
        
        # Check if all tests are disabled
        if diabled_testid and len(diabled_testid) >= len(active_testid):
            print("[save_station1_form] ERROR: All tests disabled")
            return JsonResponse({
                "status": "error",
                "message": "Please enable at least one test to proceed. All tests are currently disabled."
            }, status=400)
        
        print(f"[save_station1_form] Test mode: {test_mode} (always Sync)")
        
        # Write to Modbus registers
        try:
            print("[save_station1_form] Writing to HMI...")
            # Convert to int and handle potential conversion errors
            try:
                open_deg_int = int(float(open_degree_s1)) if open_degree_s1 is not None else 0
                close_deg_int = int(float(close_degree_s1)) if close_degree_s1 is not None else 0
            except (ValueError, TypeError) as e:
                print(f"[save_station1_form] ERROR converting degree values: {e}")
                return JsonResponse({
                    "status": "error",
                    "message": f"Invalid degree values. Open: {open_degree_s1}, Close: {close_degree_s1}"
                }, status=400)
                
            write_to_hmi(HmiAddress.S1_SET_OPEN_DEGREE, open_deg_int)
            write_to_hmi(HmiAddress.S1_SET_CLOSE_DEGREE, close_deg_int)
            print("[save_station1_form] HMI write successful")
        

        except Exception as e:
            print(f"[save_station1_form] Error writing to Modbus: {e}")
          
        
        if not fields:
            print("[save_station1_form] ERROR: No fields found")
            return JsonResponse({"error": "No fields found"}, status=400)

        # Convert list → dictionary
        field_dict = {item["name"]: item["value"] for item in fields}

        skip_keys = ["size_s1", "class_s1", "pressureunit_s1", "standard_s1", "type_s1", "body_material_s1", "VALVE_SER_NO_s1", "VALVE_SER_NO", "duration_type_s1"]
        update_fields, update_values = map_dynamic_columns(field_dict, skip_keys)

        # Add final fixed fields
        update_fields += [
            "SIZE_NAME = %s",
            "CLASS_NAME = %s",
            "PRESSURE_UNIT = %s",
            "STANDARD_NAME = %s",
            "TYPE_NAME = %s",
            "SHELL_MATERIAL_NAME = %s",
            "SYNC_NON_SYNC_STATUS = %s",
            "VALVE_SER_NO = %s",
            "STATION_STATUS = %s",
            "CYCLE_COMPLETE = %s",
            "DURATION_TYPE = %s"
        ]

        update_values += [
            field_dict.get("size_s1"),
            field_dict.get("class_s1"),
            field_dict.get("pressureunit_s1"),
            field_dict.get("standard_s1"),
            field_dict.get("type_s1"),
            field_dict.get("body_material_s1"),
            test_mode,
            field_dict.get("VALVE_SER_NO"),
            station_status,
            cycle_complete,
            field_dict.get("duration_type_s1")
        ]

        # Add WHERE ID
        update_values.append(1)

        # Build final update query
        query = f"""
            UPDATE master_temp_data
            SET {', '.join(update_fields)}
            WHERE ID = %s
        """

        print("[save_station1_form] Executing database update...")
        result = save_station(query, update_values, station_id=1)
        
        if not result:
            print("[save_station1_form] ERROR: Database update failed")
            return JsonResponse({
                "status": "error",
                "message": "Failed to save station data. Please check the logs for details."
            }, status=500)
        
        print("[save_station1_form] Database update successful")
        # Removed: Test data will be saved when clicking Next button instead
        # valve_serial_no = field_dict.get("VALVE_SER_NO")
        # insert_pressure_duration(testname,test_pressure,test_duration,active_testid,diabled_testid,pressureunit,valve_serial_no,station_number=1)

        print("[save_station1_form] Returning success response")
        return JsonResponse({"status": "success", "message": "Updated master_temp_data successfully"})

    except Exception as e:
        import traceback
        print(f"[save_station1_form] EXCEPTION: {str(e)}")
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
    
    
    
@csrf_exempt
def save_station2_form(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)

    try:
        # Check HMI connection status before saving
        hmi_connected = check_hmi_connection()
        if not hmi_connected:
            print("[save_station2_form] WARNING: HMI not connected - proceeding anyway")
            # Continue with save even if HMI is not connected
        
        data = json.loads(request.body.decode("utf-8"))

        fields = data.get("fields", [])
        field_dict = {item.get("name"): item.get("value") for item in fields}
        pressureunit = field_dict.get("pressureunit_s2")
        
        # Check if serial number is already used in another active station
        station2_serial = field_dict.get("VALVE_SER_NO_s2")
        is_duplicate, duplicate_station_id = check_duplicate_serial_station2(station2_serial)
        
        if is_duplicate:
            return JsonResponse({
                "status": "error",
                "message": f"Duplicate serial number detected! Serial number '{station2_serial}' is already used in Station {duplicate_station_id}. Please use a different serial number."
            }, status=400)
        
        station_status = "Enabled"
        cycle_complete = "No"
        testname = data.get("testname")
        test_pressure = data.get("test_pressure")
        test_duration = data.get("test_duration")
        active_testid = data.get("test_id")
        diabled_testid = data.get("diabled_testid")
        open_degree_s2 = data.get("open_degree_s2")
        close_degree_s2 = data.get("close_degree_s2")
        # Always use Sync mode (removed test_mode parameter)
        test_mode = "Sync"
        
        print(f"[DEBUG] Station 2 - Received degree values - Open: {open_degree_s2}, Close: {close_degree_s2}")
        print(f"[DEBUG] Station 2 - Test mode: {test_mode} (always Sync)")
        
        # Validate degree values
        # if open_degree_s2 is None or close_degree_s2 is None:
        #     return JsonResponse({
        #         "status": "error",
        #         "message": "Set open degree and close degree values are required but not received."
        #     }, status=400)
        
        # Check if at least one test is active (enabled)
        if not active_testid or len(active_testid) == 0:
            return JsonResponse({
                "status": "error",
                "message": "Please enable at least one test to proceed. Cannot save form without any active tests."
            }, status=400)
        
        # Check if all tests are disabled
        if diabled_testid and len(diabled_testid) >= len(active_testid):
            return JsonResponse({
                "status": "error",
                "message": "Please enable at least one test to proceed. All tests are currently disabled."
            }, status=400)
        
        # Write to Modbus registers
        try:
            # Convert to int and handle potential conversion errors
            try:
                open_deg_int = int(float(open_degree_s2)) if open_degree_s2 is not None else 0
                close_deg_int = int(float(close_degree_s2)) if close_degree_s2 is not None else 0
            except (ValueError, TypeError) as e:
                print(f"Error converting degree values to int: {e}")
                return JsonResponse({
                    "status": "error",
                    "message": f"Invalid degree values. Open: {open_degree_s2}, Close: {close_degree_s2}"
                }, status=400)
                
            # write_to_hmi(HmiAddress.S2_SET_OPEN_DEGREE, open_deg_int)
            # write_to_hmi(HmiAddress.S2_SET_CLOSE_DEGREE, close_deg_int)

        except Exception as e:
            print(f"Error writing to Modbus: {e}")
        
        if not fields:
            return JsonResponse({"error": "No fields found"}, status=400)

        # Convert list → dictionary
        field_dict = {item["name"]: item["value"] for item in fields}

        skip_keys = ["size_s2", "class_s2", "pressureunit_s2", "standard_s2", "type_s2", "body_material_s2", "VALVE_SER_NO_s2", "VALVE_SER_NO", "duration_type_s2"]
        update_fields, update_values = map_dynamic_columns(field_dict, skip_keys)

        # Add final fixed fields
        update_fields += [
            "SIZE_NAME = %s",
            "CLASS_NAME = %s",
            "PRESSURE_UNIT = %s",
            "STANDARD_NAME = %s",
            "TYPE_NAME = %s",
            "SHELL_MATERIAL_NAME = %s",
            "SYNC_NON_SYNC_STATUS = %s",
            "VALVE_SER_NO = %s",
            "STATION_STATUS = %s",
            "CYCLE_COMPLETE = %s",
            "DURATION_TYPE = %s"
        ]

        update_values += [
            field_dict.get("size_s2"),
            field_dict.get("class_s2"),
            field_dict.get("pressureunit_s2"),
            field_dict.get("standard_s2"),
            field_dict.get("type_s2"),
            field_dict.get("body_material_s2"),
            test_mode,
            field_dict.get("VALVE_SER_NO_s2"),
            station_status,
            cycle_complete,
            field_dict.get("duration_type_s2")
        ]

        # Add WHERE ID
        update_values.append(2)

        # Build final update query
        query = f"""
            UPDATE master_temp_data
            SET {', '.join(update_fields)}
            WHERE ID = %s
        """

        result = save_station(query, update_values, station_id=2)
        
        if not result:
            return JsonResponse({
                "status": "error",
                "message": "Failed to save station data. Please check the logs for details."
            }, status=500)
        
        # Removed: Test data will be saved when clicking Next button instead
        # valve_serial_no_s2 = field_dict.get("VALVE_SER_NO_s2")
        # insert_pressure_duration(testname,test_pressure,test_duration,active_testid,diabled_testid,pressureunit,valve_serial_no_s2,station_number=2)
        return JsonResponse({"status": "success", "message": "Updated master_temp_data successfully"})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


