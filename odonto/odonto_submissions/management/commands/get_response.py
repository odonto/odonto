"""
Send a test message to the upstream web service
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth


RESPONSES_URL = "https://ebusiness.dpb.nhs.uk/responses.asp"


class Command(BaseCommand):

    def handle(self, *args, **options):
        response = requests.get(
            RESPONSES_URL,
            auth=HTTPBasicAuth(settings.DPB_USERNAME, settings.DPB_PASSWORD),
        )
        print(response.content)
