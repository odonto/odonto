"""
Load the users for Odonto
"""
import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from opal.models import UserProfile, Role

from odonto.models import PerformerNumber

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            help="Specify import file",
        )

    def handle(self, *args, **options):
        with open(options.get("file_name")) as csvfile:
            reader = csv.reader(csvfile)
            for first, last, performer_number, email in reader:
                first = first.strip()
                last = last.strip()
                username = '{}.{}'.format(
                    first.lower()[0],
                    last.lower().replace('’', '')
                )
                user = User(
                    username=username,
                    first_name=first,
                    last_name=last,
                    email=email
                )
                user.set_password('whoops')
                user.save()
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.force_password_change = False
                profile.save()

                if performer_number:
                    PerformerNumber.objects.create(
                        number=performer_number,
                        user=user
                    )
