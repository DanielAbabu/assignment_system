from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from logs.models import AuditLog
import re
from django.contrib import messages
from .models import Assignment
from .forms import AssignmentForm
from submissions.models import Submission
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

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
            # Save ManyToMany relationships (students)
            form.save_m2m()
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


@login_required
def edit_assignment(request, pk):
    if request.user.role != 'teacher':
        return HttpResponseForbidden()
    assignment = get_object_or_404(Assignment, pk=pk, teacher=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.save()
            form.save_m2m()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('teacher_dashboard')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignments/create.html', {'form': form, 'assignment': assignment})


@login_required
@require_POST
def delete_assignment(request, pk):
    if request.user.role != 'teacher':
        return HttpResponseForbidden()
    assignment = get_object_or_404(Assignment, pk=pk, teacher=request.user)
    title = assignment.title
    assignment.delete()
    messages.success(request, f"Assignment '{title}' deleted.")
    return redirect('teacher_dashboard')


@login_required
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    # Only the teacher who owns the assignment can grade
    if request.user.role != 'teacher' or submission.assignment.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == 'POST':
        grade = request.POST.get('grade', '').strip()

        # Validate: accept numeric (0-100) or letter grades like A, B+, C- etc.
        valid = False
        if grade == '':
            valid = True
            normalized = None
        else:
            # numeric
            try:
                val = float(grade)
                if 0 <= val <= 100:
                    normalized = str(int(val)) if val.is_integer() else str(val)
                    valid = True
            except Exception:
                normalized = None
            # letter grades
            if not valid:
                if re.match(r'^[A-Fa-f][\+\-]?$', grade):
                    normalized = grade.upper()
                    valid = True

        if not valid:
            messages.error(request, 'Invalid grade. Use 0-100 or letter grades like A, B+, C-')
            return redirect('view_submissions', pk=submission.assignment.pk)

        old = submission.grade
        submission.grade = normalized
        submission.save()
        # Audit log entry when grade changed
        if old != submission.grade:
            ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
            action = f"Grade changed for {submission.student.email} on '{submission.assignment.title}': {old} -> {submission.grade}"
            AuditLog.objects.create(user=request.user, action=action, ip_address=ip)
        messages.success(request, f"Graded {submission.student.name}: {submission.grade}")
    return redirect('view_submissions', pk=submission.assignment.pk)