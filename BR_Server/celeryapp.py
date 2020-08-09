from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BR_Server.settings')

app = Celery('BR_Server')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'America/Montreal'

#Runs the script to identify new members follow-up dates and sends emails
#to staff to follow-up with those members
app.conf.beat_schedule = {
    'member-check-everyday': {
        'task':'BR_Server.tasks.member_email',
        'schedule': crontab(hour=6, minute=0),
    }
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))