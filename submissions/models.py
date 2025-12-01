from django.db import models
from assignments.models import Assignment
from users.models import User
import os

def submission_upload_path(instance, filename):
    # Files stored as: media/assignments/assignment_id/student_id_filename.ext
    return f'assignments/{instance.assignment.id}/{instance.student.id}_{filename}'

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    file = models.FileField(upload_to=submission_upload_path)
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'student')  # One submission per student per assignment
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.email} - {self.assignment.title}"

    def filename(self):
        return os.path.basename(self.file.name)