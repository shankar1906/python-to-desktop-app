from django.urls import path
from standard_app.views.api_views.cycle_complete_api_views import save_station_api, global_save_api, download_excel_api

urlpatterns = [
    path('save_station/', save_station_api, name='save_station_api'),
    path('global_save/', global_save_api, name='global_save_api'),
    path('download_excel/', download_excel_api, name='download_excel_api'),
]
