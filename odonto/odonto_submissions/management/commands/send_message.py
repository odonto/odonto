"""
Send a test message to the upstream web service
"""
from django.core.management.base import BaseCommand
from odonto.odonto_submissions import models
from opal.models import Episode


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('episode_id', type=int)

    def handle(self, *args, **options):
        episode = Episode.objects.get(id=options['episode_id'])
        print("sending episode {}".format(episode.id))
        submission = models.Submission.send(episode)
        print("submission state: {}".format(submission.state))
        print("submission response: {}".format(submission.response))

