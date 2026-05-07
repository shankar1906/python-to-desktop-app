from django.urls import path
from standard_app.views.pages.standards_page_views import standard_list_page

urlpatterns = [
    path("standards/", standard_list_page, name="standard_list"),
]
