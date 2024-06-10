from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Newsletter
from django.conf import settings
import pytz


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Newsletter.objects.filter(sent_date__lte=current_datetime).filter(status__in=['список_статусов'])

    for mailing in mailings:
        send_mail(
            subject=mailing.title,
            message=mailing.content,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing.clients.all()]
        )
        mailing.sent_date = datetime.now(zone)
        mailing.save()

    return mailings
