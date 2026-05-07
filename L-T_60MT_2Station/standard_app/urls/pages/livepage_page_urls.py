from django.urls import path
from standard_app.views.pages.livepage_page_view import livepage_page_view
from standard_app.views.pages.cycle_complete_view import cycle_complete_view

urlpatterns = [
    path('livepage/', livepage_page_view, name='livepage'),
    path('cycle_complete/', cycle_complete_view, name='cycle_complete'),
]