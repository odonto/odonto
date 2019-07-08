"""
Send a test message to the upstream web service
"""
from django.core.management.base import BaseCommand
from odonto.odonto_submissions import dpb_api



class Command(BaseCommand):

    def handle(self, *args, **options):
        response = dpb_api.get_responses()
        print(response.content)
