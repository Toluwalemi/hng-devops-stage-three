import logging
import os

from decouple import config
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from app.tasks import send_email

LOG_FILE = '/var/log/messaging_system.log'
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)


def handle_requests(request):
    """Endpoint to send email provided the parameters are valid."""
    recipient_email = request.GET.get('sendmail', "")
    talktome = request.GET.get('talktome', "").lower()
    response_messages = []

    if recipient_email:
        if validate_email_address(recipient_email):
            send_email.delay(recipient_email)
            response_messages.append(f"Email sent to {recipient_email}")
        else:
            response_messages.append(f"Invalid email address: {recipient_email}")

    if talktome == "true":
        log_message()
        response_messages.append("Current time logged")

    if response_messages:
        return JsonResponse({"message": " and ".join(response_messages)})

    return JsonResponse({"message": "No valid parameters provided"})

def validate_email_address(email):
    """Validate email address"""
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def log_message():
    current_time = timezone.now()
    logging.info(f"[hng-stage-three] Current time: {current_time}")


def retrieve_logs(request):
    with open(LOG_FILE, 'r') as file:
        logs = file.read()
    return HttpResponse(logs, content_type='text/plain')
