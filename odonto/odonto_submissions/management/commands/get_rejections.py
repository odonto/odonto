"""
Get's a csv of episodes that cannot be processed by compass
"""
import csv
import os
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from opal.models import Episode
from opal.core import serialization
from odonto.episode_categories import FP17Episode, FP17OEpisode
from odonto.odonto_submissions import serializers


REJECTIONS_FILE = os.path.join("..", "rejections.csv")
UNSUBMITTED_FILE = os.path.join("..", "unsubmitted.csv")


class Command(BaseCommand):

    def get_row(self, episode, rejection_reason):
        sub_link = episode.category.get_submit_link()
        abs_sub_link = f"{settings.HOST_NAME_AND_PROTOCOL}{sub_link}"
        return {
            "category": episode.category_name,
            "date": episode.category.get_sign_off_date(),
            "location": episode.fp17dentalcareprovider_set.get().provider_location_number,
            "performer": episode.fp17dentalcareprovider_set.get().performer,
            "submit_link": abs_sub_link,
            "rejection_reason": rejection_reason
        }

    def get_rejected_row(self, episode):
        return self.get_row(episode, episode.category.submission().rejection)

    def get_serialize_error_row(self, episode):
        row = None
        try:
            self.serialize_episode(episode)
        except Exception as e:
            row = self.get_row(episode, e)
        return row

    def serialize_episode(self, episode):
        serializers.translate_episode_to_xml(episode, 1, 1, 1)

    def get_acceptances_without_referrals(self):
        return FP17OEpisode.get_submitted_episodes().exclude(
            orthodonticassessment__date_of_assessment=None
        ).filter(orthodonticassessment__date_of_referral=None)

    def get_rows_without_a_performer(self):
        category_names = [
            FP17Episode.display_name,
            FP17OEpisode.display_name
        ]
        episodes = Episode.objects.filter(
            category_name__in=category_names
        ).filter(
            fp17dentalcareprovider__performer=None
        ).filter(
            stage=FP17Episode.OPEN
        )
        result = []
        for episode in episodes:
            result.append(self.get_row(episode, "No performer recorded"))
        return result

    def get_old_unsubmitted_fp17s_rows(self):
        THIRTY_DAYS_AGO = datetime.date.today() - datetime.timedelta(30)
        episodes = Episode.objects.filter(
            category_name=FP17Episode.display_name
        ).filter(
            stage=FP17Episode.OPEN
        ).filter(
            fp17incompletetreatment__completion_or_last_visit__lt=THIRTY_DAYS_AGO
        ).prefetch_related('fp17incompletetreatment_set')
        result = []
        for episode in episodes:
            incomplete_treatment = episode.fp17incompletetreatment_set.all()[0]
            completion_or_last_visit = incomplete_treatment.completion_or_last_visit
            err = "Episode completed on {} but not submitted".format(
                serialization.serialize_date(completion_or_last_visit)
            )
            result.append(self.get_row(episode, err))
        return result

    def get_no_completion_date_rows(self):
        SIXTY_DAYS_AGO = datetime.date.today() - datetime.timedelta(30)
        episodes = Episode.objects.filter(
            category_name=FP17Episode.display_name
        ).filter(
            stage=FP17Episode.OPEN
        ).filter(
            fp17incompletetreatment__completion_or_last_visit=None
        ).filter(
            fp17incompletetreatment__date_of_acceptance__lt=SIXTY_DAYS_AGO
        ).prefetch_related('fp17incompletetreatment_set')
        result = []
        for episode in episodes:
            incomplete_treatment = episode.fp17incompletetreatment_set.all()[0]
            acceptance_date = incomplete_treatment.date_of_acceptance
            result.append(self.get_row(
                episode, "Episode has not completion date and is not submitted but episode was accepted on {}".format(
                    serialization.serialize_date(acceptance_date)
                )
            ))
        return result

    def handle(self, *args, **kwargs):
        with open(REJECTIONS_FILE, 'w', newline='') as csvfile:
            fieldnames = [
                'date',
                'category',
                'location',
                'performer',
                'submit_link',
                'rejection_reason'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            for episode in FP17Episode.get_rejected_episodes():
                writer.writerow(self.get_rejected_row(episode))

            for episode in FP17OEpisode.get_rejected_episodes():
                writer.writerow(self.get_rejected_row(episode))

            for episode in FP17Episode.get_submitted_episodes().filter(submission=None):
                serialize_error_row = self.get_serialize_error_row(episode)
                if serialize_error_row:
                    writer.writerow(serialize_error_row)

            for episode in FP17OEpisode.get_submitted_episodes().filter(submission=None):
                serialize_error_row = self.get_serialize_error_row(episode)
                if serialize_error_row:
                    writer.writerow(serialize_error_row)

            writer.writerow({})

            for episode in self.get_acceptances_without_referrals():
                writer.writerow(self.get_row(episode, "Referral date required"))

            for row in self.get_rows_without_a_performer():
                writer.writerow(row)

            for row in self.get_old_unsubmitted_fp17s_rows():
                writer.writerow(row)

            for row in self.get_no_completion_date_rows():
                writer.writerow(row)
