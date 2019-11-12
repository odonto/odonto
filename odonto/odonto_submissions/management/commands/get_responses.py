"""
Get's the latest 'response' from which we can get the result of
submissions processed so far from Compass.

Then send an email with the current summary of the status quo so far.
"""
import json
import traceback
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from opal.core.serialization import OpalSerializer
from odonto.odonto_submissions.models import Response, Submission
from odonto.episode_categories import FP17Episode, FP17OEpisode
from odonto.odonto_submissions import logger


class Command(BaseCommand):
    def send_email(self, response):
        context = {"summary": {}}
        successful = response.get_successfull_submissions()
        rejected = Submission.objects.filter(
            id__in=[i.id for i in response.get_rejected_submissions().keys()]
        )
        fp17_category = FP17Episode.display_name
        fp17o_category = FP17OEpisode.display_name
        context["summary"]["Latest response"] = {
            "FP17 Success": successful.filter(episode__category_name=fp17_category).count(),
            "FP17 Rejected": rejected.filter(episode__category_name=fp17_category).count(),
            "FP17O Success": successful.filter(episode__category_name=fp17o_category).count(),
            "FP17O Rejected": rejected.filter(episode__category_name=fp17o_category).count(),
        }
        context["summary"]["FP17"] = FP17Episode.summary()
        context["summary"]["FP17O"] = FP17Episode.summary()
        today = datetime.date.today()
        title = f"Odonto response information for {today}"
        context["title"] = title
        html_message = render_to_string("emails/response_summary.html", context)
        plain_message = strip_tags(html_message)
        admin_emails = ", ".join([i[1] for i in settings.ADMINS])
        logger.info(f"sending email {title} to {admin_emails}")
        logger.info(json.dumps(context, indent=4, cls=OpalSerializer))
        send_mail(
            title,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            settings.ADMINS,
            html_message=html_message,
        )

    def handle(self, *args, **options):
        try:
            response = Response.get()
            response.update_submissions()
            self.send_email(response)
        except Exception as e:
            logger.info(f"Sending failed to get responses with {e}")
            logger.info(traceback.format_exc())
            logger.error('Failed to get responses')

