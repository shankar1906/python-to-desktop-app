from django.http import JsonResponse
from standard_app.decorators import permission_required
from standard_app.services.gauge_details_service import (
    get_all_gauges,
    get_next_gauge_id,
    insert_gauge,
    update_gauge,
    delete_gauge_record,
    check_duplicate_serial,
    count_enabled_gauges_by_station
)
from datetime import datetime


@permission_required("Gauge Details")
def get_all_gauges_api(request):
    """
    GET endpoint to retrieve all gauges.
    Returns JSON array of gauges.
    """
    if request.method != "GET":
        return JsonResponse({"error": "Invalid method"}, status=405)
    
    rows = get_all_gauges()
    
    gauges_list = []
    for r in rows:
        gd_done_date = r[6]
        gd_due_date = r[7]
        
        gauges_list.append({
            "gd_id": r[0],
            "gd_serial_number": r[1],
            "gd_medium": r[2],
            "gd_pressure_range_psi": r[3],
            "gd_pressure_range_bar": r[4],
            "gd_pressure_range_kgcm2": r[5],
            "gd_done_date": gd_done_date.strftime('%Y-%m-%d') if gd_done_date else '',
            "gd_due_date": gd_due_date.strftime('%Y-%m-%d') if gd_due_date else '',
            "gd_station_id": r[8],
            "gd_status": r[9],
        })
    
    existing_serials = [g["gd_serial_number"] for g in gauges_list if g["gd_serial_number"]]
    
    # Get superuser level from session
    superuser_level = request.session.get("superuser", 0)
    
    return JsonResponse({
        "gauges": gauges_list,
        "existing_serials": existing_serials,
        "superuser_level": superuser_level
    })


def _parse_date(date_str):
    if not date_str or date_str.strip() == '':
        return None
    try:
        return datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
    except:
        return None


@permission_required("Gauge Details")
def delete_gauge_api(request, pk):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)
    
    delete_gauge_record(pk)
    return JsonResponse({"success": True, "message": "Gauge deleted successfully"})


def check_serial_exists_api(request):
    """API to check if serial number exists (for real-time validation)"""
    serial = request.GET.get("serial", "").strip()
    exclude_id = request.GET.get("exclude_id", "").strip()
    
    if not serial:
        return JsonResponse({"exists": False})
    
    exclude_id_int = None
    if exclude_id:
        try:
            exclude_id_int = int(exclude_id)
        except:
            pass
    
    exists = check_duplicate_serial(serial, exclude_id_int)
    return JsonResponse({"exists": bool(exists)})


@permission_required("Gauge Details")
def save_gauges_api(request):
    """API to save all gauge rows (bulk save)"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        # Extract all rows from form
        gd_ids = request.POST.getlist('gd_id[]')
        serials = request.POST.getlist('gd_serial_number[]')
        mediums = request.POST.getlist('gd_medium[]')
        range_psis = request.POST.getlist('gd_pressure_range_psi[]')
        range_bars = request.POST.getlist('gd_pressure_range_bar[]')
        range_kgcm2s = request.POST.getlist('gd_pressure_range_kgcm2[]')
        done_dates = request.POST.getlist('gd_done_date[]')
        due_dates = request.POST.getlist('gd_due_date[]')
        station_ids = request.POST.getlist('gd_station_id[]')
        statuses = request.POST.getlist('gd_status[]')

        # Validate duplicate serial numbers within form
        serial_map = {}
        for i in range(len(serials)):
            serial = serials[i].strip()
            if serial:
                gd_id = ''
                try:
                    gd_id = gd_ids[i].strip()
                except (IndexError, ValueError):
                    pass
                
                if serial.lower() in serial_map:
                    return JsonResponse({"error": f'Duplicate serial number "{serial}" in form'}, status=400)
                serial_map[serial.lower()] = (i, gd_id)

        # Validate against database
        for serial, (idx, current_id) in serial_map.items():
            exclude_id = int(current_id) if current_id else None
            if check_duplicate_serial(serial, exclude_id):
                return JsonResponse({"error": f'Serial number "{serial}" already exists in database'}, status=400)

        # Validate station counts
        station_counts = {}
        for i in range(len(serials)):
            station_id_str = station_ids[i].strip() if i < len(station_ids) else ''
            status_str = statuses[i].strip() if i < len(statuses) else ''
            
            if station_id_str and status_str == '1':  # Check for enabled (value '1')
                try:
                    station_id_int = int(station_id_str)
                    station_counts[station_id_int] = station_counts.get(station_id_int, 0) + 1
                except:
                    pass
        
        for station_id_int, count in station_counts.items():
            if count > 10:
                return JsonResponse({"error": f'Station {station_id_int} has {count} enabled rows. Max 10 allowed.'}, status=400)

        # Process each row
        for i in range(len(serials)):
            serial = serials[i].strip()
            medium = mediums[i].strip() if i < len(mediums) else ''
            range_psi = range_psis[i].strip() if i < len(range_psis) else ''
            range_bar = range_bars[i].strip() if i < len(range_bars) else ''
            range_kgcm2 = range_kgcm2s[i].strip() if i < len(range_kgcm2s) else ''
            done_date = _parse_date(done_dates[i]) if i < len(done_dates) else None
            due_date = _parse_date(due_dates[i]) if i < len(due_dates) else None
            
            try:
                station_id = int(station_ids[i]) if i < len(station_ids) and station_ids[i].strip() else None
            except:
                station_id = None

            try:
                status = int(statuses[i]) if i < len(statuses) and statuses[i].strip() else 0
            except:
                status = 0

            # Get or generate GD_ID
            try:
                gd_id = int(gd_ids[i]) if i < len(gd_ids) and gd_ids[i].strip() else None
            except:
                gd_id = None

            # Skip empty rows
            if not serial and not medium and not range_psi and not range_bar and not range_kgcm2 and not station_id:
                continue

            if gd_id:
                # Update existing
                update_gauge(gd_id, serial, medium, range_psi, range_bar, range_kgcm2, 
                           done_date, due_date, station_id, status)
            else:
                # Insert new
                if serial or medium or range_psi or range_bar or range_kgcm2 or station_id:
                    insert_gauge(serial, medium, range_psi, range_bar, range_kgcm2,
                               done_date, due_date, station_id, status)

        return JsonResponse({"success": True, "message": "Gauge details saved successfully"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
