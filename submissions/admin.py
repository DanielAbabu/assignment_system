from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'grade')
    list_filter = ('assignment__teacher', 'submitted_at')
    search_fields = ('student__email', 'assignment__title')