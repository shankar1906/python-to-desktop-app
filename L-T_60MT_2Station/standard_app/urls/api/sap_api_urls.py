from django.urls import path
from standard_app.views.api.sap_api_views import (
    get_sap_data_api,
)

urlpatterns = [
    path("get_sap_data/", get_sap_data_api, name="api_get_sap_data"),
]
