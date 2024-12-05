from celery import Celery

app = Celery('project_name')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
