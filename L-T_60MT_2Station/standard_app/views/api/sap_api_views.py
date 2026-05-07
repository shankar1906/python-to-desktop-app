from django.http import JsonResponse
from standard_app.decorators import login_required
from standard_app.services.sap_service import (
    get_sap_data
)
import json
import re

@login_required
def get_sap_data_api(request):
    if request.method == 'GET':
        serial_no = request.GET.get('serial_no')
        try:
            data = get_sap_data(serial_no)
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)