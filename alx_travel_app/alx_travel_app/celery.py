# alx_travel_app/celery.py
import os
import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")
django.setup()  

app = Celery("alx_travel_app")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
