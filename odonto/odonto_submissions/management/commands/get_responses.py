"""
Get all responses that have been processed.

Notably this is not all processes but just the processes
that have been processed since the last time this has
run.
"""
from django.core.management.base import BaseCommand
from odonto.odonto_submissions import dpb_api


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = dpb_api.get_responses()
        print(response.content)
