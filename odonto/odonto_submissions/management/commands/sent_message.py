"""
Send a test message to the upstream web service
"""
from django.core.management.base import BaseCommand
from odonto.odonto_submissions.models import BCDS1Message
from opal.models import Episode


# episode_ids = [9, 13]


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('episode_id', type=int)

    def handle(self, *args, **options):
        episode = Episode.objects.get(id=options['episode_id'])
        message, _ = BCDS1Message.objects.get_or_create(episode=episode)
        message.new_submission()
        message.send()
