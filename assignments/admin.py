from django.contrib import admin
from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'deadline', 'created_at')
    list_filter = ('teacher', 'deadline')
    search_fields = ('title', 'teacher__email')