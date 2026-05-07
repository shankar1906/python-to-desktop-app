import os

from django.contrib import messages
from django.http import FileResponse
from django.shortcuts import render

from standard_app.decorators import permission_required
from standard_app.services.merged_graph_pdf_service import build_merged_graph_pdf
from standard_app.services.pressure_analysis_serial_service import (
    distinct_valve_serial_numbers_from_pressure_analysis,
)


@permission_required("Graph")
def graph_page(request):
    serial_numbers = distinct_valve_serial_numbers_from_pressure_analysis()

    if request.method == "POST":
        valve_serial = (request.POST.get("valve_serial") or "").strip()
        if not valve_serial:
            messages.error(request, "Please select a valve serial number.")
            return render(request, "graph.html", {"serial_numbers": serial_numbers})

        result = build_merged_graph_pdf(valve_serial)
        if not result.get("ok"):
            messages.error(request, result.get("error") or "Could not generate merged graph PDF.")
            return render(request, "graph.html", {"serial_numbers": serial_numbers})

        path = result.get("path")
        if not path or not os.path.isfile(path):
            messages.error(request, "PDF was not written to disk.")
            return render(request, "graph.html", {"serial_numbers": serial_numbers})

        try:
            return FileResponse(
                open(path, "rb"),
                as_attachment=True,
                filename=os.path.basename(path),
            )
        except OSError as e:
            messages.error(request, str(e))
            return render(request, "graph.html", {"serial_numbers": serial_numbers})

    return render(request, "graph.html", {"serial_numbers": serial_numbers})
