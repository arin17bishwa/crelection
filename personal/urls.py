from django.urls import path

from .views import (
    home_view,
    results_view,
)

app_name='personal'

urlpatterns = [
    path('',home_view,name='home'),
    path('results/',results_view,name='results'),
]
