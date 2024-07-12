import logging
import os
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.utils import timezone

# Configure logging
LOG_FILE = '/var/log/messaging_system.log'
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)


def handle_requests(request):
    sendmail = request.GET.get('sendmail', "")
    talktome = request.GET.get('talktome', "")

    response_messages = []

    if sendmail:
        send_email(sendmail)
        response_messages.append(f"Email sent to {sendmail}")

    if talktome:
        log_message()
        response_messages.append("Current time logged")

    if response_messages:
        return JsonResponse({"message": " and ".join(response_messages)})

    return JsonResponse({"message": "No valid parameters provided"})


def send_email(recipient):
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        [recipient],
        fail_silently=False,
    )


def log_message():
    current_time = timezone.now()
    logging.info(f"[hng-stage-three] Current time: {current_time}")


def retrieve_logs(request):
    with open(LOG_FILE, 'r') as file:
        logs = file.read()
    return HttpResponse(logs, content_type='text/plain')
