"""
Send a test message to the upstream web service
"""
import json
from datetime import date
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from odonto.odonto_submissions import models
from odonto.episode_categories import FP17Episode, FP17OEpisode
from opal.models import Episode
from odonto.odonto_submissions import logger


class Command(BaseCommand):
    def get_fp17o_qs(self):
        episodes = (
            Episode.objects.filter(category_name=FP17OEpisode.display_name)
            .filter(stage="Submitted")
            .filter(submission=None)
        )

        # we currently are only sending down a subset
        return (
            episodes.exclude(patient__demographics__ethnicity_fk_id=None)
            .exclude(orthodonticassessment__date_of_assessment=None)
            .exclude(orthodonticassessment__date_of_referral=None)
            .filter(orthodontictreatment__date_of_completion=None)
        )

    def get_fp17_qs(self):
        return (
            Episode.objects.filter(category_name=FP17Episode.display_name)
            .filter(stage="Submitted")
            .filter(submission=None)
        )

    def send_submission(self, episode, success_count, failure_count):
        logger.info(f"Sending {episode.id}")
        try:
            models.Submission.send(episode)
            success_count += 1
        except Exception as e:
            logger.info(f"Sending failed for Episode {episode.id} with {e}")
            failure_count += 1
        return success_count, failure_count

    def send_email(
        self,
        fp17_success_count,
        fp17_failure_count,
        fp17o_success_count,
        fp17o_failure_count,
    ):
        successes = fp17_success_count + fp17o_success_count
        failures = fp17_failure_count + fp17o_failure_count
        today = date.today()
        threshold_breached = False
        title = f"Submissions {today}"

        if failures > settings.FAILED_TO_SEND_WARNING_THRESHOLD:
            title = f"URGENT: {failures} submissions failed to send on {today}"
            threshold_breached = True

        context = {
            "title": title,
            "threshold_breached": threshold_breached,
            "total_success": successes,
            "total_failure": failures,
            "fp17_success_count": fp17_success_count,
            "fp17_failure_count": fp17_failure_count,
            "fp17o_success_count": fp17o_success_count,
            "fp17o_failure_count": fp17o_failure_count,
        }
        html_message = render_to_string("emails/submission_sent.html", context)
        plain_message = strip_tags(html_message)
        logger.info(f"sending email to {','.join(settings.ADMINS)}")
        logger.info(json.dumps(context, indent=4))
        send_mail(
            title,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            settings.ADMINS,
            html_message=html_message,
        )

    def handle(self, *args, **options):
        fp17_success_count = 0
        fp17_failure_count = 0

        fp17o_success_count = 0
        fp17o_failure_count = 0
        fp17s = self.get_fp17_qs()
        fp17os = self.get_fp17o_qs()
        for episode in fp17s:
            fp17_success_count, fp17_failure_count = self.send_submission(
                episode, fp17_success_count, fp17_failure_count
            )
        for episode in fp17os:
            fp17o_success_count, fp17o_failure_count = self.send_submission(
                episode, fp17o_success_count, fp17o_failure_count
            )

        self.send_email(
            fp17_success_count,
            fp17_failure_count,
            fp17o_success_count,
            fp17o_failure_count,
        )
