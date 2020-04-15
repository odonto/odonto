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
    def get_fp17os(self):
        return FP17OEpisode.get_submitted_episodes().filter(submission=None).filter(
            patient__demographics__protected=False
        )

    def get_fp17_qs(self):
        return FP17Episode.get_submitted_episodes().filter(submission=None).filter(
            patient__demographics__protected=False
        )

    def send_submission(self, episode):
        logger.info(f"Sending {episode.id}")
        try:
            models.Submission.send(episode)
        except Exception as e:
            logger.info(f"Sending failed for Episode {episode.id} with {e}")
            logger.info(traceback.format_exc())

    def handle(self, *args, **options):
        fp17s = self.get_fp17_qs()
        fp17os = self.get_fp17os()
        for episode in fp17s:
            self.send_submission(
                episode
            )

        for episode in fp17os:
            self.send_submission(
                episode
            )

