from django.shortcuts import render
from standard_app.decorators import permission_required


@permission_required("Gauge Details")
def gauge_details_page(request):
    """
    Render the gauge details page.
    Data will be fetched via API call from frontend JavaScript.
    """
    # Get superuser level from session
    superuser_level = request.session.get('superuser', 0)
    try:
        superuser_level = int(superuser_level)
    except (ValueError, TypeError):
        superuser_level = 0
    
    return render(request, "gauge_details.html", {
        'superuser_level': superuser_level
    })
