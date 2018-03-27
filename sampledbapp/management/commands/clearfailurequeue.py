from django.core.management.base import BaseCommand, CommandError
from sampledbapp.models import *
import django_rq
from datetime import datetime
import logging

# Loop through the fail queue and update the Job model status
class Command (BaseCommand):

    def handle(self, *args, **options):

        queue = django_rq.get_queue('failed')
        queue.empty()

        logger = logging.getLogger('django')

        log_string = "Fail queue emptied - " + str(datetime.now()) + " \n"

       # print log_string

        logger.info(log_string)
