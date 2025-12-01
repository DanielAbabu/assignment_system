from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('create/', views.create_assignment, name='create_assignment'),
    path('<int:pk>/submissions/', views.view_submissions, name='view_submissions'),
]