from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from standard_app.decorators import permission_required
import json
from standard_app.services.form_service import get_testname
from standard_app.views.api.configuration_api_views import TestleadSmartsyncx
from standard_app.src import HmiAddress
import traceback
    
    
@csrf_exempt
@permission_required("form")
def get_pressure_duration(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            standard = data.get("standard")
            valve_size = data.get("size")
            valve_class = data.get("class")
            valve_type = data.get("type")
            shell_material = data.get("body_material")
            pressure_unit = data.get("pressure_unit")
            station = data.get("station")
            
            # Validate required fields
            if not all([standard, valve_size, valve_class, valve_type, shell_material, pressure_unit]):
                return JsonResponse({
                    "error": "Missing required fields. Please fill all testing parameters."
                }, status=400)
            
            try:
                test_name, pressure, duration, test_ids, degree = get_testname(
                    standard, valve_size, valve_type, shell_material, valve_class
                )
            except ValueError as ve:
                # Handle specific validation errors from get_testname
                return JsonResponse({
                    "error": str(ve)
                }, status=400)
            except Exception as e:
                # Handle database or other errors
                return JsonResponse({
                    "error": f"Database error: {str(e)}",
                    "details": traceback.format_exc()
                }, status=500)
            
            # Check for None values in the results
            if not test_name or not pressure or not duration:
                return JsonResponse({
                    "error": "No test data found for the selected combination."
                }, status=400)
            
            if pressure_unit.lower() == "psi":
                try:
                    pressure = [float(p) * 14.5 if p is not None else None for p in pressure]
                    invalid = [i for i, p in enumerate(pressure) if p is None]
                    
                    if invalid:
                        return JsonResponse({
                            "error": f"Pressure contains NULL values at positions: {invalid}. Check test configuration."
                        }, status=400)
                except (TypeError, ValueError) as e:
                    return JsonResponse({
                        "error": f"Invalid pressure value: {str(e)}"
                    }, status=400)

            pressure_duration = {
                "test_name": test_name,
                "pressure": pressure,
                "duration": duration,
                "testid": test_ids,
                "degree": degree
            }
            return JsonResponse({"pressure_duration": pressure_duration})
        else:
            return JsonResponse({
                "error": "Method not allowed. Use POST."
            }, status=405)

    except json.JSONDecodeError as e:
        return JsonResponse({
            "error": "Invalid JSON in request body",
            "details": str(e)
        }, status=400)

    except Exception as e:
        # Catch-all for any unexpected errors
        return JsonResponse({
            "error": "Unexpected server error",
            "details": str(e),
            "traceback": traceback.format_exc()
        }, status=500)


def get_syncstatus(request):
    # Always use Sync Mode (no longer reading from HMI)
    sync_status = 1  # 1 = Sync Mode
    return JsonResponse({"status": "success", "syncstatus": sync_status})


@csrf_exempt
@permission_required("form")
def validate_psr_unit(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            station_id = data.get("station_id")
            psr_unit = data.get("psr_unit")
            
            if not station_id or not psr_unit:
                 return JsonResponse({"valid": True})

            # Allow each station to use different pressure units independently
            # No validation needed - each station can have its own unit
            return JsonResponse({"valid": True})

    except Exception as e:
        return JsonResponse({
            "error": "Validation error",
            "details": str(e)
        }, status=500)