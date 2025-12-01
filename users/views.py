from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import StudentRegistrationForm, TeacherRegistrationForm, LoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'users/register_student.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Teacher account created!')
            return redirect('dashboard')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'users/register_teacher.html', {'form': form})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')