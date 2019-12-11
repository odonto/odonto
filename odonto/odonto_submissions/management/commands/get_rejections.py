"""
Get's a csv of episodes that cannot be processed by compass
"""
import csv
import os
from django.core.management.base import BaseCommand
from odonto.episode_categories import FP17Episode, FP17OEpisode


FILE_NAME = os.path.join("..", "rejections.csv")


class Command(BaseCommand):
    def get_row(self, episode):
        return {
            "category": episode.category_name,
            "location": episode.fp17dentalcareprovider_set.get().provider_location_number,
            "submit_link": episode.category.get_submit_link(),
            "rejection_reason": episode.category.submission().rejection
        }

    def handle(self, *args, **kwargs):
        with open(FILE_NAME, 'w', newline='') as csvfile:
            fieldnames = [
                'category',
                'location',
                'submit_link',
                'rejection_reason'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            for episode in FP17Episode.get_rejected_episodes():
                writer.writerow(self.get_row(episode))

            for episode in FP17OEpisode.get_rejected_episodes():
                writer.writerow(self.get_row(episode))

