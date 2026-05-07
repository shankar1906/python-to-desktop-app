from django.urls import path
from standard_app.views.api_views.livepage_api_views import (
    get_active_testbtn_api,
    get_size_class_api,
    get_pressure_duration_api,
    get_pressure_data_api,
    start_test_thread_api,
    stop_test_thread_api,
    stop_pressure_collection_only_api,
    update_pressure_analysis_api,
    reset_test_api,
    get_automode_response_api,
    get_machine_mode_api,
    reset_all_api,
    toggle_station_api,
    get_station_status_api
)

urlpatterns = [
    path('get_active_testbtn/', get_active_testbtn_api, name='get_active_testbtn_api'),
    path('get_size_class/', get_size_class_api, name='get_size_class_api'),
    path('get_pressure_duration/<int:test_id>', get_pressure_duration_api, name='get_pressure_duration'),
    path('stop_test_thread/', stop_test_thread_api, name='stop_test_thread_api'),
    path('stop_pressure_collection_only/', stop_pressure_collection_only_api, name='stop_pressure_collection_only_api'),
    path('get_pressure_data/', get_pressure_data_api, name='get_pressure_data_api'),
    path('start_test_thread/', start_test_thread_api, name='start_test_thread'),
    path('update_pressure_analysis/', update_pressure_analysis_api, name='update_pressure_analysis'),
    path('reset_test/<int:test_id>/', reset_test_api, name='reset_test_api'),
    path('get_machine_mode/', get_machine_mode_api, name='get_machine_mode'),
    path('get_automode_response/', get_automode_response_api, name='get_automode_response_api'),
    path('reset_all/', reset_all_api, name='reset_all_api'),
    path('toggle_station/', toggle_station_api, name='toggle_station_api'),
    path('get_station_status/', get_station_status_api, name='get_station_status_api'),
]