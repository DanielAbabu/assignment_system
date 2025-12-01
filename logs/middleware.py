from .models import AuditLog

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated:
            return response

        path = request.path
        method = request.method

        # Log important actions
        important_paths = [
            '/login/', '/logout/', '/register/', '/create/', '/submit/', '/download/'
        ]

        if any(p in path for p in important_paths) or method != 'GET':
            ip = self.get_client_ip(request)
            AuditLog.objects.create(
                user=request.user,
                action=f"{method} {path}",
                ip_address=ip
            )

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')