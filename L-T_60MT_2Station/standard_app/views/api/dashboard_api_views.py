from django.http import JsonResponse
from standard_app.services.dashboard_service import check_incomplete_test,delete_test
from standard_app.services.user_config_service import get_integration_mode
from django.views.decorators.csrf import csrf_exempt
# api
def check_incomplete_test_api(request):
    data = check_incomplete_test()


    if(data):
        return JsonResponse({
            "status": 'Found',
            "data": data,
        })
    else:
        return JsonResponse({
            "status": "No Data Found",
        })
        
@csrf_exempt
def delete_test_api(request):
    data = request.POST.get('valve_ser_no')
    delete_data = delete_test(data)
    if(delete_data):
        return JsonResponse({
            "status": 'Success',
        })
    else:
        return JsonResponse({
            "status": 'Failed',
        })


def get_new_test_route_api(request):
    integration_mode = str(get_integration_mode() or "2").strip()
    route = "/sap_form/" if integration_mode == "1" else "/form/"

    return JsonResponse({
        "status": "success",
        "integration_mode": integration_mode,
        "route": route,
    })

