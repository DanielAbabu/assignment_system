from django import forms
from django.utils import timezone
from .models import Assignment
from users.models import User

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'deadline', 'allowed_extensions', 'students']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='student'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
        help_text='Select students who should see this assignment.'
    )

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        if deadline < timezone.now():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline