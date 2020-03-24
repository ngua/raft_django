from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail


logger = get_task_logger(__name__)


@task(name='send_email_async')
def send_email_async(subject, message, **kwargs):
    logger.info('Email sent via celery')
    return send_mail(subject, message, **kwargs)
