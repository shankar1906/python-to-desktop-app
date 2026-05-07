from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from standard_app.services.item_details_service import ItemDetailsService
import json

@require_http_methods(["GET"])
def get_item_details_api(request):
    try:
        data = ItemDetailsService.get_all_item_details()
        return JsonResponse({"success": True, "data": data, "message": "Item details fetched successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["POST"])
def add_item_detail_api(request):
    try:
        data = request.POST.dict()
        data['is_mandatory'] = request.POST.get('is_mandatory') == 'on'
        data['is_top_header'] = request.POST.get('is_top_header') == 'on'
        
        ItemDetailsService.add_item_detail(data)
        return JsonResponse({"success": True, "message": "Item detail added successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["POST"])
def update_item_detail_api(request, detail_id):
    try:
        data = request.POST.dict()
        data['is_mandatory'] = request.POST.get('is_mandatory') == 'on'
        data['is_top_header'] = request.POST.get('is_top_header') == 'on'
        
        ItemDetailsService.update_item_detail(detail_id, data)
        return JsonResponse({"success": True, "message": "Item detail updated successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["POST"])
def delete_item_detail_api(request, detail_id):
    try:
        ItemDetailsService.delete_item_detail(detail_id)
        return JsonResponse({"success": True, "message": "Item detail deleted successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["POST"])
def bulk_delete_item_details_api(request):
    try:
        body = json.loads(request.body)
        detail_ids = body.get('ids', [])
        ItemDetailsService.bulk_delete_item_details(detail_ids)
        return JsonResponse({"success": True, "message": "Item details deleted successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_http_methods(["GET"])
def get_unique_labels_api(request):
    try:
        labels = ItemDetailsService.get_all_unique_row_labels()
        return JsonResponse({"success": True, "labels": labels})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
