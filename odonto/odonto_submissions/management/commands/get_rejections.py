"""
Get's a csv of episodes that cannot be processed by compass
"""
import csv
import os
from django.core.management.base import BaseCommand
from odonto.episode_categories import FP17Episode, FP17OEpisode
from odonto.odonto_submissions import serializers


FILE_NAME = os.path.join("..", "rejections.csv")


class Command(BaseCommand):
    def get_rejected_row(self, episode):
        return {
            "category": episode.category_name,
            "date": episode.category.get_sign_off_date(),
            "location": episode.fp17dentalcareprovider_set.get().provider_location_number,
            "submit_link": episode.category.get_submit_link(),
            "rejection_reason": episode.category.submission().rejection
        }

    def serialize_episode(self, episode):
        serializers.translate_episode_to_xml(episode, 1, 1, 1)

    def get_serialize_error_row(self, episode):
        try:
            self.serialize_episode(episode)
        except Exception as e:
            return {
                "category": episode.category_name,
                "date": episode.category.get_sign_off_date(),
                "location": episode.fp17dentalcareprovider_set.get().provider_location_number,
                "submit_link": episode.category.get_submit_link(),
                "rejection_reason": f"{e.__class__} {e}"
            }


    def handle(self, *args, **kwargs):
        with open(FILE_NAME, 'w', newline='') as csvfile:
            fieldnames = [
                'date',
                'category',
                'location',
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