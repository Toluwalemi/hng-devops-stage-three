from django.urls import path
from .views import handle_requests, retrieve_logs

urlpatterns = [
    path('send-email/', handle_requests, name='handle_requests'),
    path('logs/', retrieve_logs, name='retrieve_logs'),
]
