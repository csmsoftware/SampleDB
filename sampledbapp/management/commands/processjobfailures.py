from django.core.management.base import BaseCommand, CommandError
from sampledbapp.models import *
import django_rq
from datetime import datetime
import logging

# Loop through the fail queue and update the Job model status
class Command (BaseCommand):

    def handle(self, *args, **options):

        logger = logging.getLogger('django')

        queue = django_rq.get_queue('failed')

        jobs = Job.objects.filter(rq_id__in=queue.job_ids,status__in=[1,2])

       # print queue.job_ids

        for job in jobs:

            rq_job = queue.fetch_job(job.rq_id)

            job.rq_exception = rq_job.exc_info

            if job.job_type == "commit_staging_samples":

                job.text_to_show = " Staging commit failed - contact support \n\n " \
                                   " Exception thrown: \n " + rq_job.exc_info + " \n\n " \
                                   " Staging json: \n " + job.text_to_show

            else:

                job.text_to_show = " Task failed - contact support \n\n " \
                                   " Exception thrown: \n " + rq_job.exc_info


            job.status = 3
            job.datetime_failed = datetime.now()

            job.save()

            log_string = "+ --------------------------------------------------------------- + \n\n" \
                         " Sample DB user task failed. \n\n " \
                         "  job_type: " + str(job.job_type) + " \n " \
                         "  Datetime created: " + str(job.datetime_created) + " \n " \
                         "  Datetime run: " + str(job.datetime_run) + " \n " \
                         "  Datetime failed: " + str(job.datetime_failed) + " \n " \
                         "  job.id: " + str(job.pk) + " \n " \
                         "  user.id: " + str(job.user.id) + " \n " \
                         "  rq_id: " + str(job.rq_id) + " \n " \
                         "  Exception: \n" + str(job.rq_exception) + " \n " \
                         "+ --------------------------------------------------------------- + \n"

            print (log_string)

            logger.error(log_string)
