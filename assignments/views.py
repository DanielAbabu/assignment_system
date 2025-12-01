from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Assignment
from .forms import AssignmentForm
from submissions.models import Submission

@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden("Only teachers can access this page.")
    assignments = Assignment.objects.filter(teacher=request.user)
    return render(request, 'assignments/teacher_dashboard.html', {
        'assignments': assignments
    })

@login_required
def create_assignment(request):
    if request.user.role != 'teacher':
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = request.user
            assignment.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('teacher_dashboard')
    else:
        form = AssignmentForm()
    
    return render(request, 'assignments/create.html', {'form': form})

@login_required
def view_submissions(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, teacher=request.user)
    submissions = Submission.objects.filter(assignment=assignment).select_related('student')
    return render(request, 'assignments/submissions_list.html', {
        'assignment': assignment,
        'submissions': submissions
    })