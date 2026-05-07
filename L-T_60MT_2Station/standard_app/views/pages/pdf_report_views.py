from django.shortcuts import render
from django.shortcuts import render
from standard_app.decorators import permission_required

@permission_required("Graph")
def pdf_report(request):
    return render(request, "pdf_report.html")