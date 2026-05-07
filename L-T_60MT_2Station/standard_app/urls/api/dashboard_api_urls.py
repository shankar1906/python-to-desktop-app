from django.urls import path
from standard_app.views.api.dashboard_api_views import check_incomplete_test_api, delete_test_api, get_new_test_route_api

urlpatterns = [
    path('check_incomplete_test/', check_incomplete_test_api, name='dashboard_check_incomplete_test'),
    path('delete_test/', delete_test_api, name='dashboard_delete_test'),
    path('get_new_test_route/', get_new_test_route_api, name='dashboard_get_new_test_route'),
]