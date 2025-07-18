from django.utils.timezone import now
from ip_tracking.models import RequestLog

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Get path
        path = request.path

        # Create log entry
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=path
        )

        # Process the request
        response = self.get_response(request)
        return response