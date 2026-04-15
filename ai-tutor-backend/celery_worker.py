import os
from celery import Celery

def make_celery(app_name=__name__):
    celery = Celery(
        app_name,
        backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
        broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    )
    return celery

celery_app = make_celery()
