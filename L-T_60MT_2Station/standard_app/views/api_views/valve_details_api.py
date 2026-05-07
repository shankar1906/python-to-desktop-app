from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from standard_app.services.valve_details_service import ValveDetailsService
import json

@require_http_methods(["GET"])
def get_valve_details_api(request):
    try:
        data = ValveDetailsService.get_all_valve_details()
        return JsonResponse({"success": True, "data": data, "message": "Valve details fetched successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["POST"])
def add_valve_detail_api(request):
    try:
        data = request.POST.dict()
        # Handle checkboxes which might not be in the POST if unchecked
        data['is_mandatory'] = request.POST.get('is_mandatory') == 'on'
        data['is_top_header'] = request.POST.get('is_top_header') == 'on'
        
        ValveDetailsService.add_valve_detail(data)
        return JsonResponse({"success": True, "message": "Valve detail added successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["POST"])
def update_valve_detail_api(request, detail_id):
    try:
        data = request.POST.dict()
        data['is_mandatory'] = request.POST.get('is_mandatory') == 'on'
        data['is_top_header'] = request.POST.get('is_top_header') == 'on'
        
        ValveDetailsService.update_valve_detail(detail_id, data)
        return JsonResponse({"success": True, "message": "Valve detail updated successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["POST"])
def delete_valve_detail_api(request, detail_id):
    try:
        ValveDetailsService.delete_valve_detail(detail_id)
        return JsonResponse({"success": True, "message": "Valve detail deleted successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["POST"])
def bulk_delete_valve_details_api(request):
    try:
        body = json.loads(request.body)
        detail_ids = body.get('ids', [])
        ValveDetailsService.bulk_delete_valve_details(detail_ids)
        return JsonResponse({"success": True, "message": "Valve details deleted successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
