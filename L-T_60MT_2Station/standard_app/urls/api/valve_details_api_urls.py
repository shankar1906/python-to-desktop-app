from django.urls import path
from standard_app.views.api_views.valve_details_api import (
    get_valve_details_api, add_valve_detail_api, update_valve_detail_api,
    delete_valve_detail_api, bulk_delete_valve_details_api
)

urlpatterns = [
    path('valve_details/', get_valve_details_api, name='get-valve-details-api'),
    path('valve_details/add/', add_valve_detail_api, name='add-valve-detail-api'),
    path('valve_details/edit/<int:detail_id>/', update_valve_detail_api, name='update-valve-detail-api'),
    path('valve_details/delete/<int:detail_id>/', delete_valve_detail_api, name='delete-valve-detail-api'),
    path('valve_details/bulk_delete/', bulk_delete_valve_details_api, name='bulk-delete-valve-details-api'),
]
