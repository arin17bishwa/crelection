from django.urls import path

from .views import (
    registration_view,
    logout_view,
    login_view,
    must_authenticate_view,
    activate,
)

app_name='account'

urlpatterns = [
    path('login/',login_view,name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('must-authenticate/', must_authenticate_view, name='must_authenticate'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]
