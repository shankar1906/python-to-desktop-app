from django.urls import path
from standard_app.views.page_views.item_details import item_details_page

urlpatterns = [
    path('item_details/', item_details_page, name='item-details'),
]
