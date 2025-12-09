from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.conf import settings
from assignments.models import Assignment
from .models import Submission
import os
from logs.models import AuditLog
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return HttpResponseForbidden("Access denied.")

    # Show assignments assigned to this student OR assignments with no explicit student list
    all_assignments = Assignment.objects.filter(Q(students=request.user) | Q(students__isnull=True)).distinct().order_by('-created_at')
    my_submissions = Submission.objects.filter(student=request.user)
    submitted_assignment_ids = my_submissions.values_list('assignment_id', flat=True)

    return render(request, 'submissions/student_dashboard.html', {
        'assignments': all_assignments,
        'submitted_ids': submitted_assignment_ids,
        'my_submissions': my_submissions,
    })


@login_required
def student_assignments_json(request):
    """Return JSON list of assignments for the logged-in student."""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Access denied'}, status=403)

    assignments = Assignment.objects.filter(Q(students=request.user) | Q(students__isnull=True)).distinct().order_by('-created_at')
    my_submissions = Submission.objects.filter(student=request.user)
    submitted_ids = set(my_submissions.values_list('assignment_id', flat=True))

    data = []
    for a in assignments:
        data.append({
            'id': a.id,
            'title': a.title,
            'description': a.description[:200],
            'deadline': a.deadline.isoformat() if a.deadline else None,
            'is_expired': a.is_expired(),
            'teacher': a.teacher.name if a.teacher else str(a.teacher.email),
            'submitted': a.id in submitted_ids,
        })

    return JsonResponse({'assignments': data, 'now': timezone.now().isoformat()})

@login_required
def submit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    if request.user.role != 'student':
        return HttpResponseForbidden()

    if assignment.is_expired():
        messages.error(request, "Deadline has passed. You cannot submit.")
        return redirect('student_dashboard')

    # Check if already submitted
    existing = Submission.objects.filter(assignment=assignment, student=request.user).first()

    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        ext = os.path.splitext(uploaded_file.name)[1].lower()

        allowed = assignment.get_allowed_extensions_list()
        if ext not in allowed:
            messages.error(request, f"File type {ext} not allowed. Allowed: {assignment.allowed_extensions}")
            return render(request, 'submissions/submit.html', {'assignment': assignment})

        if uploaded_file.size > settings.MAX_UPLOAD_SIZE:
            messages.error(request, "File too large. Maximum 10MB allowed.")
            return render(request, 'submissions/submit.html', {'assignment': assignment})

        # Delete old submission if exists (resubmit = replace)
        if existing:
            if os.path.exists(existing.file.path):
                os.remove(existing.file.path)
            existing.delete()

        Submission.objects.create(
            assignment=assignment,
            student=request.user,
            file=uploaded_file
        )
        messages.success(request, "Assignment submitted successfully!")
        return redirect('student_dashboard')

    return render(request, 'submissions/submit.html', {
        'assignment': assignment,
        'existing': existing
    })

@login_required
def download_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    if request.user != submission.assignment.teacher:
        return HttpResponseForbidden("You can only download submissions for your own assignments.")

    # Audit log
    AuditLog.objects.create(
        user=request.user,
        action=f"Downloaded submission: {submission.filename()} by {submission.student.email}"
    )

    response = HttpResponse(submission.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{submission.filename()}"'
    return response