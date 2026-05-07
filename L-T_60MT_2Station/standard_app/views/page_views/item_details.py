from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required # Uncomment if login is required
def item_details_page(request):
    context = {
        'page_title': 'Item Details',
        'header_title': 'Item Details'
    }
    return render(request, 'standard_app/item_details.html', context)
