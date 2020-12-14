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

SEND_ALL_AFTER_DATE = date(2020, 4, 1)


class Command(BaseCommand):
    def get_fp17os(self):
        return FP17OEpisode.get_submitted_episodes()

    def get_fp17_qs(self):
        return FP17Episode.get_submitted_episodes()

    def filter_for_new_or_failed_since(self, qs):
        to_send = []
        failed_states = set([
            models.Submission.FAILED_TO_SEND, models.Submission.REJECTED_BY_COMPASS
        ])
        for episode in qs:
            sign_off_date = episode.category.get_sign_off_date()
            if sign_off_date and sign_off_date < SEND_ALL_AFTER_DATE:
                continue
            submission = episode.category.submission()
            if not submission or submission.state in failed_states:
                to_send.append(episode)
        return to_send

    def send_submission(self, episode):
        logger.info(f"Sending {episode.id}")
        try:
            models.Submission.send(episode)
        except Exception as e:
            logger.info(f"Sending failed for Episode {episode.id} with {e}")
            logger.info(traceback.format_exc())

    def handle(self, *args, **options):
        fp17s = self.filter_for_new_or_failed_since(self.get_fp17_qs())
        fp17os = self.filter_for_new_or_failed_since(self.get_fp17os())
        for episode in fp17s:
            self.send_submission(
                episode
            )

        for episode in fp17os:
            self.send_submission(
                episode
            )

