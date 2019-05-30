"""
Send a test message to the upstream web service
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
POST_URL = "https://ebusiness.dpb.nhs.uk/claims.asp"


class Command(BaseCommand):

    def handle(self, *args, **options):
        payload = ""
        response = requests.post(
            POST_URL,
            auth=HTTPBasicAuth(settings.DPB_USERNAME, settings.DPB_PASSWORD),
            data=payload
        )
        import ipdb; ipdb.set_trace()
        print(response)
