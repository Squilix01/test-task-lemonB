from celery import Celery
from celery.schedules import crontab
from settings.config import config


celery_app = Celery(
    "lemon_b",
    broker=config.redis.get_url(),
    backend=config.redis.get_url(),
    include=["tasks.workers"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "scrape-amazon-every-6-hours": {
        "task": "tasks.workers.scrape_amazon_task",
        "schedule": crontab(minute=0, hour="*/6"),
    },
}
