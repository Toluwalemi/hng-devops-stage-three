from celery import shared_task
from django.core.mail import send_mail
from decouple import config


@shared_task
def send_email(recipient_email):
    send_mail(
        'Toluwalemi: HNG DevOps Stage Three',
        'Here is a confirmation that this works :)',
        config("EMAIL_HOST_USER", cast=str, default=""),
        [recipient_email],
        fail_silently=False,
    )