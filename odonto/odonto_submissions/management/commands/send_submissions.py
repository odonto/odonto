import json
import traceback
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
        episodes = FP17OEpisode.get_submitted_episodes().filter(submission=None)
        # we currently are only sending down a subset based on...

        # 1. Before demographics was made mandatory some patients were
        # added without demogrphaics so skip those.

        # 2 there are essentialy, logic for FP17Os when treatment
        # is complete is still in development
        # just send down those who have been assessed for the time
        # being.

        # 3. Referral is requires if there is an assessment, again
        # some fp17os have been created without this. So we
        # exclude those for the time being.
        return (
            episodes.exclude(patient__demographics__ethnicity_fk_id=None)
            .exclude(orthodonticassessment__date_of_assessment=None)
            .exclude(orthodonticassessment__date_of_referral=None)
            .filter(orthodontictreatment__date_of_completion=None)
        )

    def get_fp17_qs(self):
        return FP17Episode.get_submitted_episodes().filter(submission=None)

    def send_submission(self, episode):
        logger.info(f"Sending {episode.id}")
        try:
            models.Submission.send(episode)
        except Exception as e:
            logger.info(f"Sending failed for Episode {episode.id} with {e}")
            logger.info(traceback.format_exc())
            return False
        return True

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
        admin_emails = ", ".join([i[1] for i in settings.ADMINS])
        logger.info(f"sending email to {admin_emails}")
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
            successful = self.send_submission(
                episode
            )
            if successful:
                fp17_success_count += 1
            else:
                fp17_failure_count += 1

        for episode in fp17os:
            successful = self.send_submission(
                episode
            )
            if successful:
                fp17o_success_count += 1
            else:
                fp17o_failure_count += 1

        self.send_email(
            fp17_success_count,
            fp17_failure_count,
            fp17o_success_count,
            fp17o_failure_count,
        )
