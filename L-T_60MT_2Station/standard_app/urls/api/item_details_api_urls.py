from django.urls import path
from standard_app.views.api_views.item_details_api import (
    get_item_details_api, add_item_detail_api, update_item_detail_api,
    delete_item_detail_api, bulk_delete_item_details_api, get_unique_labels_api
)

urlpatterns = [
    path('item_details/', get_item_details_api, name='get-item-details-api'),
    path('item_details/add/', add_item_detail_api, name='add-item-detail-api'),
    path('item_details/edit/<int:detail_id>/', update_item_detail_api, name='update-item-detail-api'),
    path('item_details/delete/<int:detail_id>/', delete_item_detail_api, name='delete-item-detail-api'),
    path('item_details/bulk_delete/', bulk_delete_item_details_api, name='bulk-delete-item-details-api'),
    path('item_details/unique_labels/', get_unique_labels_api, name='get-unique-labels-api'),
]
