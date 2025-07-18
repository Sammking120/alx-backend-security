from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from ip_tracking.models import RequestLog, SuspiciousIP
from django.db import models

@shared_task
def detect_anomalies():
    # Define sensitive paths
    sensitive_paths = ['/admin', '/login']
    
    # Time window: last hour
    one_hour_ago = now() - timedelta(hours=1)
    
    # Get IPs with request counts in the last hour
    ip_counts = RequestLog.objects.filter(timestamp__gte=one_hour_ago).values('ip_address').annotate(
        request_count=models.Count('ip_address')
    )
    
    # Check for IPs exceeding 100 requests/hour
    for ip_data in ip_counts:
        if ip_data['request_count'] > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip_data['ip_address'],
                defaults={'reason': f"Exceeded 100 requests/hour: {ip_data['request_count']} requests"}
            )
    
    # Check for IPs accessing sensitive paths
    sensitive_requests = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address').distinct()
    
    for ip_data in sensitive_requests:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip_data['ip_address'],
            defaults={'reason': f"Accessed sensitive path in {sensitive_paths}"}
        )