from django.utils.timezone import now
from django.http import HttpResponseForbidden
from django.core.cache import cache
from ip_tracking.models import RequestLog, BlockedIP
from ipgeolocation import IPGeolocation # type: ignore

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geo = IPGeolocation()

    def __call__(self, request):
        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access forbidden: Your IP is blocked.")

        # Get geolocation data from cache or API
        cache_key = f"geo_{ip_address}"
        geo_data = cache.get(cache_key)
        if not geo_data:
            try:
                geo_data = self.geo.get_geolocation(ip_address)
                cache.set(cache_key, geo_data, 86400)  # Cache for 24 hours
            except Exception as e:
                geo_data = {'country': None, 'city': None}  # Fallback in case of API failure

        # Get path
        path = request.path

        # Create log entry
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=path,
            country=geo_data.get('country'),
            city=geo_data.get('city')
        )

        # Process the request
        response = self.get_response(request)
        return response