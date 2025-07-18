from django.db import models

class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)  # Supports IPv4 and IPv6
    timestamp = models.DateTimeField()
    path = models.CharField(max_length=2000)  # Standard max URL length

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"