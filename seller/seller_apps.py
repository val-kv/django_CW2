from django.apps import AppConfig
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.schedulers import DjangoScheduler
from .scheduler import send_mailing


class SellerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seller'

    def ready(self):
        scheduler = DjangoScheduler(DjangoJobStore(), {})
        scheduler.add_job(send_mailing, 'interval', seconds=10)
        scheduler.start()