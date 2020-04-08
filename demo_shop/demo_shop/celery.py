import os
from celery import Celery

# set the default Django settings module for the 'celery' programm.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_shop.settings')

app = Celery('demo_shop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()