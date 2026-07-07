from celery import Celery
from celery.schedules import crontab


celery = Celery(
    "trekking_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.update(
    result_backend="redis://localhost:6379/0",
    broker_connection_retry_on_startup=True,
    imports=("tasks",)
)

celery.conf.beat_schedule = {
    "daily-trek-reminder": {
        "task": "tasks.daily_trek_reminder",
        "schedule": crontab(hour=8, minute=0),
    }
}