from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('students/', views.students_list, name='students_list'),
    path('', views.dashboard, name='dashboard'),
]