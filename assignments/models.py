from django.db import models
from users.models import User
from django.utils import timezone

class Assignment(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(User, blank=True, related_name='assignments', limit_choices_to={'role': 'student'})
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()
    allowed_extensions = models.CharField(
        max_length=255,
        default='.pdf,.docx,.zip,.jpg,.jpeg,.png,.txt',
        help_text="Comma-separated extensions (e.g. .pdf,.docx)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_expired(self):
        return timezone.now() > self.deadline

    def get_allowed_extensions_list(self):
        return [ext.strip().lower() for ext in self.allowed_extensions.split(',') if ext.strip()]