from django.urls import path
from standard_app.views.pages.sap_form_page_views import sap_form_page


urlpatterns = [
    path("sap_form/", sap_form_page, name="sap_form_page"),
]
