from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from opal.models import UserProfile


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        user = User(username='super')
        user.set_password('super1')
        user.is_superuser = True
        user.is_staff = True
        user.first_name = "super"
        user.surname = "ohc"
        user.save()
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.force_password_change = False
        profile.save()

        user = User(username='dentist')
        user.first_name = "Diana"
        user.surname = "Dent"
        user.set_password('dentist1')
        user.save()
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.force_password_change = False
        profile.save()
        user.performernumber_set.create(
            number="111"
        )

        user = User(username='nurse')
        user.first_name = "Norma"
        user.surname = "Nur"
        user.set_password('nurse1')
        user.save()
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.force_password_change = False
        profile.save()