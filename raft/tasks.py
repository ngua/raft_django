from django.core.mail import send_mail
from django.utils.module_loading import import_string
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from djmoney import settings


logger = get_task_logger(__name__)


@task(name='send_email_async')
def send_email_async(subject, message, **kwargs):
    logger.info('Email sent via celery')
    return send_mail(subject, message, **kwargs)


@periodic_task(run_every=(crontab(minute=0, hour=0)))
def update_rates(backend=settings.EXCHANGE_BACKEND, **kwargs):
    backend = import_string(backend)()
    backend.update_rates(**kwargs)
