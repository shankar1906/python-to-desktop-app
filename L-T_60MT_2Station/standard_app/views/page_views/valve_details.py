from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required # Uncomment if login is required
def valve_details_page(request):
    context = {
        'page_title': 'Valve Details',
        'header_title': 'Valve Details'
    }
    return render(request, 'standard_app/valve_details.html', context)
