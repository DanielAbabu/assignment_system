from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('create/', views.create_assignment, name='create_assignment'),
    path('<int:pk>/edit/', views.edit_assignment, name='edit_assignment'),
    path('<int:pk>/delete/', views.delete_assignment, name='delete_assignment'),
    path('<int:pk>/submissions/', views.view_submissions, name='view_submissions'),
    path('grade/<int:submission_id>/', views.grade_submission, name='grade_submission'),
]