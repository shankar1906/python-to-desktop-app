import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from standard_app.services.cycle_complete_service import save_station_service, global_save_service

@csrf_exempt
def save_station_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            station_id = data.get('station_id')
            extra_fields = data.get('extra_fields', {})
            
            if not station_id:
                return JsonResponse({'status': 'error', 'message': 'Station ID is required'}, status=400)
                
            success = save_station_service(station_id, extra_fields)
            if success:
                return JsonResponse({'status': 'success', 'message': f'Station {station_id} saved successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to save station data'}, status=400)
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def global_save_api(request):
    if request.method == 'POST':
        try:
            result = global_save_service()
            if isinstance(result, dict) and result.get("success"):
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Cycle completed successfully',
                    'excel_urls': result.get("excel_urls", [])
                })
            elif result is True:
                return JsonResponse({'status': 'success', 'message': 'Cycle completed successfully', 'excel_urls': []})
            else:
                return JsonResponse({'status': 'error', 'message': 'No data to save or operation failed'}, status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

import os
from django.http import HttpResponse, Http404

def download_excel_api(request):
    filename = request.GET.get('file')
    if not filename:
        raise Http404("No file specified")
        
    export_dir = r"C:\Users\infot\Downloads"
    filepath = os.path.join(export_dir, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        raise Http404("File not found")
