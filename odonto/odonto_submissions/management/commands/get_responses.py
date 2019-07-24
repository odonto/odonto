"""
Get all responses that have been processed.

Notably this is not all processes but just the processes
that have been processed since the last time this has
run.
"""
from django.core.management.base import BaseCommand
from odonto.odonto_submissions.models import CompassBatchResponse
from odonto.odonto_submissions import dpb_apik


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = CompassBatchResponse.get()
        print(response.content)
