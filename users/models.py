from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

def validate_school_email(value):
    if not value.lower().endswith('@aastu.edu.et'):
        raise ValidationError('Only @aastu.edu.et email addresses are allowed.')

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    email = models.EmailField(
        unique=True,
        validators=[validate_school_email],
        error_messages={'unique': "A user with that email already exists."},
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email