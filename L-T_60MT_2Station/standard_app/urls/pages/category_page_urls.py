from django.urls import path
from standard_app.views.pages.category_page_views import category


urlpatterns = [

    path('category/', category, name='category'),

]
