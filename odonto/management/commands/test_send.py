"""
Send a test message to the upstream web service
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth
from odonto_submissions.serializers import get_bcds1
from opal.models import Episode



POST_URL = "https://ebusiness.dpb.nhs.uk/claims.asp"


class Command(BaseCommand):

    def handle(self, *args, **options):
        episode_id = 1
        contract_number = 1000000000
        location_id = 10108
        pin = 1111
        payload = ""
        response = requests.post(
            POST_URL,
            auth=HTTPBasicAuth(settings.DPB_USERNAME, settings.DPB_PASSWORD),
            data=payload
        )
        serializer = serializers.FP17Serializer(episode, user)
        serializer.save()
        print(response)
