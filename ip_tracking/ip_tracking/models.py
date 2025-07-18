from django.db import models

class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)  # Supports IPv4 and IPv6
    timestamp = models.DateTimeField()
    path = models.CharField(max_length=2000)  # Standard max URL length
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"

class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)  # Supports IPv4 and IPv6

    def __str__(self):
        return self.ip_address

class SuspiciousIP(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)  # Supports IPv4 and IPv6
    reason = models.TextField()
    flagged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"