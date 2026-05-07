from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
from standard_app.services.form_service import get_status, get_station_data, compare_station_data
from standard_app.services.save_station1_service import save_common_test_data
from standard_app.src import HmiAddress
from standard_app.views.api.configuration_api_views import TestleadSmartsyncx
import traceback


def write_to_hmi(address, value):
    """Write value to HMI register"""
    try:
        if TestleadSmartsyncx is None:
            print(f"[HMI WRITE ERROR] HMI connection not established.")
            return False
        TestleadSmartsyncx.write_register(address, value)
        print(f"[HMI WRITE] Address {address} = {value}")
        return True
    except Exception as e:
        print(f"[HMI WRITE ERROR] Address {address}: {e}")
        return False

def _extract_first_number(value, default=0):
    try:
        if value is None:
            return default
        s = str(value)
        num = ""
        for ch in s:
            if ch.isdigit():
                num += ch
            elif num:
                break
        return int(num) if num else default
    except Exception:
        return default


@csrf_exempt
def continue_station1(request):
    try:
        station_num = 1  # This is station 1
        
        # Get test data from request if POST method
        if request.method == "POST":
            data = json.loads(request.body.decode("utf-8"))
            testname = data.get("testname")
            test_pressure = data.get("test_pressure")
            test_duration = data.get("test_duration")
            active_testid = data.get("test_id")
            disabled_testid = data.get("disabled_testid")
            pressureunit = data.get("pressureunit")
            
            # Ensure extra tests are always present (SAP provides N tests; we add 2 more)
            # 29 = Hydro seat B (copy from testId 2)
            # 49 = Air seat B   (copy from testId 4)
            try:
                ids_raw = list(active_testid or [])
                ids_int = [int(x) for x in ids_raw]
                if testname and test_pressure and test_duration and len(testname) == len(ids_int):
                    # Find exact base indices from the incoming payload.
                    # No fallback to other testIds (copy ONLY from the specified base IDs).
                    def _idx(tid: int):
                        try:
                            return ids_int.index(tid)
                        except ValueError:
                            return None

                    has29 = 29 in ids_int
                    has49 = 49 in ids_int

                    i2 = _idx(2)
                    if i2 is not None:
                        if not has29:
                            # add duplicate
                            active_testid.append(29)
                            testname.append("Hydro seat B")
                            test_pressure.append(test_pressure[i2])
                            test_duration.append(test_duration[i2])
                            ids_int.append(29)
                        else:
                            # force-sync existing 29 values from base test 2
                            i29 = _idx(29)
                            if i29 is not None:
                                testname[i29] = "Hydro seat B"
                                test_pressure[i29] = test_pressure[i2]
                                test_duration[i29] = test_duration[i2]

                    i4 = _idx(4)
                    if i4 is not None:
                        if not has49:
                            # add duplicate
                            active_testid.append(49)
                            testname.append("Air seat B")
                            test_pressure.append(test_pressure[i4])
                            test_duration.append(test_duration[i4])
                            ids_int.append(49)
                        else:
                            # force-sync existing 49 values from base test 4
                            i49 = _idx(49)
                            if i49 is not None:
                                testname[i49] = "Air seat B"
                                test_pressure[i49] = test_pressure[i4]
                                test_duration[i49] = test_duration[i4]
            except Exception as e:
                print(f"[continue_station1] Could not auto-add extra tests: {e}")

            # Save common test data for all active stations
            if testname and test_pressure and test_duration and active_testid and pressureunit:
                save_common_test_data(testname, test_pressure, test_duration, active_testid, disabled_testid or [], pressureunit)
                print(f"[continue_station{station_num}] Test data saved successfully")
        
        # Get valve size and class from master_temp_data (actual values)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT SIZE_NAME, CLASS_NAME
                FROM master_temp_data
                WHERE ID = %s
            """, [station_num])
            result = cursor.fetchone()
            
            if result:
                size_name = result[0]
                class_name = result[1]

                valve_size_value = _extract_first_number(size_name, default=0)
                valve_class_value = _extract_first_number(class_name, default=0)
                
                print(f"[continue_station{station_num}] Writing to HMI - Valve Size: {valve_size_value}, Valve Class: {valve_class_value}")
                
                # Write valve size and class values to shared HMI addresses (same for all stations)
                write_to_hmi(HmiAddress.VALVE_SIZE_ID, int(valve_size_value))
                write_to_hmi(HmiAddress.VALVE_CLASS_ID, int(valve_class_value))

                # Enable all stations
                write_to_hmi(HmiAddress.S1_STATUS, 1)
                write_to_hmi(HmiAddress.S2_STATUS, 1)
                
                # Write initial test parameters and enable the station
                if data and testname and test_pressure and test_duration:
                    try:
                        # Extract first test only
                        first_p = float(test_pressure[0]) if test_pressure else 0
                        first_t = int(test_duration[0]) if test_duration else 0
                        first_id = int(active_testid[0]) if active_testid else 0
                        
                        # Handle unit conversion (Sync with livepage logic)
                        if pressureunit == 'BAR':
                            first_p = first_p * 10
                            
                        # Write global test parameters (Registers 2006, 2007, 2008)
                        write_to_hmi(HmiAddress.SET_PRESSURE, int(first_p))
                        write_to_hmi(HmiAddress.SET_TIME, int(first_t))
                        write_to_hmi(HmiAddress.TEST_TYPE, first_id)
                        
                        print(f"[continue_station1] Initial test parameters & Status written to HMI")
                    except Exception as he:
                        print(f"[continue_station1] HMI Parameter write error: {he}")
            else:
                print(f"[continue_station{station_num}] No data found in master_temp_data")
        
        # Get status from service
        station1_status, station2_status, sync_status = get_status()
        print("station status and sync status", station1_status, station2_status, sync_status)
        
        # Always redirect to livepage (no sync/non-sync mode check)
        redirect_url = "/livepage"

        # Final consistent return
        return JsonResponse({
            "status": "success",
            "redirect_url": redirect_url,
            "station1_status": station1_status,
            "station2_status": station2_status
        })

    except Exception as e:
        print("Error in continue_station1:", e)
        print(traceback.format_exc())
        return JsonResponse({
            "status": "failure",
            "message": f"Error: {str(e)}"
        })
