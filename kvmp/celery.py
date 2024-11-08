import time
from celery import Celery
import os


celery = Celery(__name__)
celery.conf.broker_url = os.environ["CELERY_BROKER_URL"]
celery.conf.result_backend = os.environ["CELERY_RESULT_BACKEND"]


@celery.task(name="create_task")
def create_task(task_type):
    os.system('ls -l > /tmp/output.txt')
    return True