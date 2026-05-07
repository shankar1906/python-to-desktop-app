from django.urls import path
from standard_app.views.api.instrument_type_api_views import (
    get_all_instrument_types_api,
    save_instrument_types_api,
    delete_instrument_type_api,
    check_duplicate_serial_api
)

urlpatterns = [
    path("instrument_type/", get_all_instrument_types_api, name="api_get_all_instrument_types"),
    path("instrument_type/save/", save_instrument_types_api),
    path("instrument_type/delete/<int:instrument_type_id>/", delete_instrument_type_api),
    path("instrument_type/check-serial/", check_duplicate_serial_api),
]

