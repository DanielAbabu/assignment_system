from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class StudentRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user

class TeacherRegistrationForm(StudentRegistrationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))