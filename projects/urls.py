from django.urls import path
from .views import ProjectListView, ProjectDetailView, join_project
from service_hours.views import log_service_hour

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('<int:project_id>/join/', join_project, name='join_project'),
    path('<int:project_id>/log_hours/', log_service_hour, name='log_service_hour'),  # Add this line
]
