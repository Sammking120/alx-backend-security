from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ip_tracking.settings')
app = Celery('ip_tracking')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()