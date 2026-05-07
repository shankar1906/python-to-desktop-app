from django.shortcuts import render
from standard_app.decorators import permission_required

@permission_required("Graph")
def pdf_page(request):
    """
    Render the gauge details page.
    Data will be fetched via API call from frontend JavaScript.
    """
    return render(request, "pdf_regenerate.html")
