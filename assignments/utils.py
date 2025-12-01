import os
from django.http import HttpResponseForbidden
from django.conf import settings

def validate_file_upload(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in settings.ALLOWED_FILE_EXTENSIONS:
        return False, f"File type {ext} not allowed."
    if file.size > settings.MAX_UPLOAD_SIZE:
        return False, "File too large. Max 10MB."
    return True, ""