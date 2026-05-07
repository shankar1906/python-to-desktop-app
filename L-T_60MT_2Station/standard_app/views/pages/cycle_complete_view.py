from django.shortcuts import render
from django.db import connection
from ..pages.auth_page_views import _require_session_auth

def cycle_complete_view(request):
    """
    View to display the Cycle Complete results for active stations.
    """
    station_ids_str = request.GET.get('stations', '')
    station_ids = [s.strip() for s in station_ids_str.split(',') if s.strip()]
    
    stations_data = []
    
    with connection.cursor() as cursor:
        for sid in station_ids:
            # Fetch all columns dynamically to avoid missing any COL_NAME/VALUE pairs
            cursor.execute("SELECT * FROM master_temp_data WHERE ID = %s", [sid])
            row = cursor.fetchone()
            if row:
                cols = [c[0] for c in cursor.description]
                row_dict = dict(zip(cols, row))
                
                # Extract and normalize extra fields
                extra_fields = {}
                for i in range(1, 100): # Check up to COL100 just in case
                    name_col = f'COL{i}_NAME'
                    val_col = f'COL{i}_VALUE'
                    if name_col in row_dict and val_col in row_dict:
                        name = row_dict[name_col]
                        val = row_dict[val_col]
                        if name:
                            # Normalize name for dot-access: replace space/dash with underscore, lowercase
                            clean_name = name.replace(' ', '_').replace('-', '_').replace('/', '_').lower()
                            # Remove double underscores
                            while '__' in clean_name:
                                clean_name = clean_name.replace('__', '_')
                            extra_fields[clean_name.strip('_')] = val
                
                stations_data.append({
                    'id': sid,
                    'valve_ser_no': row_dict.get('VALVE_SER_NO'),
                    'pressure_unit': row_dict.get('PRESSURE_UNIT'),
                    'standard_name': row_dict.get('STANDARD_NAME'),
                    'size_name': row_dict.get('SIZE_NAME'),
                    'class_name': row_dict.get('CLASS_NAME'),
                    'type_name': row_dict.get('TYPE_NAME'),
                    'shell_material_name': row_dict.get('SHELL_MATERIAL_NAME'),
                    'extra_fields': extra_fields
                })

    context = {
        "header_title": "Cycle Complete Results",
        "username": request.session.get("username", "Guest"),
        "stations_data": stations_data,
        "bg_color": "#132039",
    }
    return render(request, "cycle_complete.html", context)
