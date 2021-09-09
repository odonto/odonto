"""
Gets the latest 'response' from which we can get the result of
submissions processed so far from Compass.
"""
import traceback
from django.core.management.base import BaseCommand
from odonto.odonto_submissions.models import Response
from odonto.odonto_submissions import logger


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            response = Response.get()
            response.update_submissions()
        except Exception as e:
            logger.info(f"Sending failed to get responses with {e}")
            logger.info(traceback.format_exc())
            logger.error('Failed to get responses')
