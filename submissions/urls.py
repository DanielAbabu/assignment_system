from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('assignments/json/', views.student_assignments_json, name='student_assignments_json'),
    path('submit/<int:pk>/', views.submit_assignment, name='submit_assignment'),
    path('download/<int:submission_id>/', views.download_submission, name='download_submission'),
]