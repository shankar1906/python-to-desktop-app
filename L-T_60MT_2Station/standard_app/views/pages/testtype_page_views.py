from django.shortcuts import render
from standard_app.decorators import permission_required
from django.db import connection
from django.contrib import messages
from django.shortcuts import render, redirect
from standard_app.services.testtype_service import *

@permission_required("Test Type")
def testtype_page(request):   
    # The page now loads data via JavaScript API calls
    # No need to pass data to template
    return render(request, "test_type.html", {})

