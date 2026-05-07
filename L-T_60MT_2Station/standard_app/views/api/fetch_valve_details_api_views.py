from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def fetch_valve_details(request):
    """
    Fetch valve details and item details from master_temp_data for a given station
    Returns all COL fields except VALVE_SER_NO
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)
    
    try:
        data = json.loads(request.body.decode("utf-8"))
        source_station_id = data.get("source_station_id")
        
        if not source_station_id:
            return JsonResponse({"error": "source_station_id is required"}, status=400)
        
        with connection.cursor() as cursor:
            # Fetch all COL fields from master_temp_data
            cursor.execute("""
                SELECT 
                    COL1_NAME, COL1_VALUE, COL2_NAME, COL2_VALUE, COL3_NAME, COL3_VALUE,
                    COL4_NAME, COL4_VALUE, COL5_NAME, COL5_VALUE, COL6_NAME, COL6_VALUE,
                    COL7_NAME, COL7_VALUE, COL8_NAME, COL8_VALUE, COL9_NAME, COL9_VALUE,
                    COL10_NAME, COL10_VALUE, COL11_NAME, COL11_VALUE, COL12_NAME, COL12_VALUE,
                    COL13_NAME, COL13_VALUE, COL14_NAME, COL14_VALUE, COL15_NAME, COL15_VALUE,
                    COL16_NAME, COL16_VALUE, COL17_NAME, COL17_VALUE, COL18_NAME, COL18_VALUE,
                    COL19_NAME, COL19_VALUE, COL20_NAME, COL20_VALUE, COL21_NAME, COL21_VALUE,
                    COL22_NAME, COL22_VALUE, COL23_NAME, COL23_VALUE
                FROM master_temp_data
                WHERE ID = %s
            """, [source_station_id])
            
            row = cursor.fetchone()
            
            if not row:
                return JsonResponse({"error": "No data found for this station"}, status=404)
            
            # Build field dictionary, excluding VALVE_SER_NO
            fields = {}
            for i in range(0, len(row), 2):
                col_name = row[i]
                col_value = row[i + 1]
                
                # Skip empty fields and VALVE_SER_NO (Serial Number)
                if col_name and col_value and col_name != "VALVE_SER_NO":
                    # Also skip if the column name is "Serial Number"
                    if col_name.lower() != "serial number":
                        fields[col_name] = col_value
            
            return JsonResponse({
                "status": "success",
                "fields": fields
            })
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
