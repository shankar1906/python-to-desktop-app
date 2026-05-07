from django.urls import path
from standard_app.views.page_views.valve_details import valve_details_page

urlpatterns = [
    path('valve_details/', valve_details_page, name='valve-details'),
]
