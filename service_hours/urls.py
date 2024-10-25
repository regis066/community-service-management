# service_hours/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log_service_hour, name='log_service_hour'),  # URL for logging hours
    path('view/', views.view_logged_hours, name='view_logged_hours'),  # URL for viewing logged hours
]
