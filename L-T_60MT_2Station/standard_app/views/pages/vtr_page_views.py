import os

from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import render

from standard_app.decorators import permission_required
from standard_app.services.excel_report_service import generate_excel_report
from standard_app.services.pressure_analysis_serial_service import (
    distinct_valve_serial_numbers_from_pressure_analysis,
    latest_count_id_for_valve,
    master_temp_data_id_for_valve,
)


@permission_required("vtr")
def vtr_page(request):
    serial_numbers = distinct_valve_serial_numbers_from_pressure_analysis()

    if request.method == "POST":
        valve_serial = (request.POST.get("valve_serial") or "").strip()
        if not valve_serial:
            messages.error(request, "Please select a valve serial number.")
            return render(request, "vtr.html", {"serial_numbers": serial_numbers})

        count_id = latest_count_id_for_valve(valve_serial)
        if count_id is None:
            messages.error(request, "No pressure_analysis data for this serial.")
            return render(request, "vtr.html", {"serial_numbers": serial_numbers})

        station_id = master_temp_data_id_for_valve(valve_serial)
        excel_url = generate_excel_report(valve_serial, count_id, station_id)
        if not excel_url:
            messages.error(
                request,
                "Excel report could not be generated (check template path and pressure_analysis data).",
            )
            return render(request, "vtr.html", {"serial_numbers": serial_numbers})

        filename = f"{valve_serial}_Count-{count_id}_report.xlsx"
        filepath = os.path.join("S:/Reports", filename)
        if not os.path.isfile(filepath):
            messages.error(request, "Report file was not found after generation.")
            return render(request, "vtr.html", {"serial_numbers": serial_numbers})

        try:
            return FileResponse(
                open(filepath, "rb"),
                as_attachment=True,
                filename=filename,
            )
        except OSError as e:
            messages.error(request, str(e))
            return render(request, "vtr.html", {"serial_numbers": serial_numbers})

    return render(request, "vtr.html", {"serial_numbers": serial_numbers})
