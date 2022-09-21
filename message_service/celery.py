import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_service.settings')
app = Celery('message_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'mailings.tasks.db_queries',
        'schedule': crontab(minute='*/1'),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
        'args': (),
    },
}
