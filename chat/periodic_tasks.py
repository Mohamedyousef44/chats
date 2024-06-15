from celery import Celery
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every 1 hours
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='*/1',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )

    PeriodicTask.objects.update_or_create(
        crontab=schedule,
        name='Update room count every 1 hour',
        task='chat.tasks.update_room_count',
        defaults={'args': json.dumps([])},
    )