from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
import random
import string
from .forms import StudentRegistrationForm, TeacherRegistrationForm, LoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            otp = ''.join(random.choices(string.digits, k=6))
            request.session['otp'] = otp
            request.session['user_id'] = user.id
            send_mail(
                'Your OTP for Login',
                f'Your OTP is: {otp}',
                'noreply@aastustudent.edu.et',
                [user.email],
                fail_silently=False,
            )
            return redirect('otp_verify')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def otp_verify(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if 'otp' not in request.session or 'user_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session['otp']:
            from .models import User
            user = User.objects.get(id=request.session['user_id'])
            login(request, user)
            del request.session['otp']
            del request.session['user_id']
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'users/otp_verify.html')

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


def students_list(request):
    """List all students — only accessible to teachers."""
    if not request.user.is_authenticated or request.user.role != 'teacher':
        return redirect('login')
    from .models import User
    students = User.objects.filter(role='student').order_by('name')
    return render(request, 'users/students_list.html', {'students': students})