from django.shortcuts import render
from standard_app.decorators import login_required
from standard_app.views.pages.form_page_views import build_form_context


@login_required
def sap_form_page(request):
    return render(request, "sap_form.html", build_form_context())
