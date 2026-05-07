from django.http import JsonResponse
from standard_app.decorators import permission_required
from standard_app.services.instrument_type_service import (
    get_all_instrument_types,
    get_next_instrument_type_id,
    insert_instrument_type,
    update_instrument_type,
    delete_instrument_type_record,
    check_duplicate_name,
    check_duplicate_serial_no
)


@permission_required("Instrument Type")
def get_all_instrument_types_api(request):
    """GET endpoint to retrieve all instrument types."""
    if request.method != "GET":
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)
    
    try:
        rows = get_all_instrument_types()
        
        instrument_types_list = []
        for row in rows:
            instrument_types_list.append({
                "instrument_type_id": row[0],
                "instrument_name": row[1],
                "instrument_serial_no": row[2],
                "instrument_done_date": str(row[3]) if row[3] else '',
                "instrument_due_date": str(row[4]) if row[4] else '',
                "status": row[6],
            })
        
        existing_names = [row[1] for row in rows]
        superuser_level = request.session.get("superuser", 0)
        
        return JsonResponse({
            "success": True,
            "instrument_types": instrument_types_list,
            "existing_names": existing_names,
            "superuser_level": superuser_level
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@permission_required("Instrument Type")
def save_instrument_types_api(request):
    """API to save all instrument type rows (bulk save)"""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

    try:
        instrument_ids = request.POST.getlist("instrument_type_id[]")
        instrument_names = request.POST.getlist("instrument_name[]")
        instrument_serial_nos = request.POST.getlist("instrument_serial_no[]")
        instrument_done_dates = request.POST.getlist("instrument_done_date[]")
        instrument_due_dates = request.POST.getlist("instrument_due_date[]")
        statuses = request.POST.getlist("status[]")

        valid_rows = [name.strip() for name in instrument_names if name.strip()]
        if not valid_rows:
            return JsonResponse({"success": False, "error": "Please enter at least one instrument name"}, status=400)

        # Validate duplicate names within form
        name_map = {}
        for i, name in enumerate(instrument_names):
            name = name.strip()
            if not name:
                continue
            if name.lower() in name_map:
                return JsonResponse({"success": False, "error": f'Duplicate instrument name "{name}" in form'}, status=400)
            name_map[name.lower()] = i

        # Process each record
        for instrument_id, instrument_name,  instrument_serial_no, instrument_done_date, instrument_due_date, status in zip(instrument_ids, instrument_names, instrument_serial_nos, instrument_done_dates, instrument_due_dates, statuses):
            instrument_name = instrument_name.strip()
            instrument_serial_no = instrument_serial_no.strip()
            instrument_done_date = instrument_done_date.strip()
            instrument_due_date = instrument_due_date.strip()
            status = status.strip()
            
            if not instrument_name:
                continue
            
            if instrument_id and instrument_id.strip():
                update_instrument_type(instrument_id, instrument_name, instrument_serial_no, instrument_done_date, instrument_due_date, status)
            else:
                next_id = get_next_instrument_type_id()
                insert_instrument_type(next_id, instrument_name, instrument_serial_no, instrument_done_date, instrument_due_date, status)

        return JsonResponse({"success": True, "message": "Instrument types saved successfully"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@permission_required("Instrument Type")
def delete_instrument_type_api(request, instrument_type_id):
    """API to delete instrument type"""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)
    
    try:
        delete_instrument_type_record(instrument_type_id)
        return JsonResponse({"success": True, "message": "Instrument type deleted successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@permission_required("Instrument Type")
def check_duplicate_serial_api(request):
    """API to check if a serial number already exists"""
    serial_no = request.GET.get('serial_no', '').strip()
    exclude_id = request.GET.get('exclude_id')
    
    if not serial_no:
        return JsonResponse({"success": True, "is_duplicate": False})
        
    exists = check_duplicate_serial_no(serial_no, exclude_id)
    return JsonResponse({
        "success": True,
        "is_duplicate": True if exists else False
    })

