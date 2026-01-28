from celery import Celery
from app.settings import settings

celery_app = Celery(
    "people_counter",
    broker=settings.RABBITMQ_URL,
    backend=settings.RESULT_BACKEND,
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    worker_prefetch_multiplier=1,
)

import app.tasks  # noqa: F401
