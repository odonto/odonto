"""
Send a test message to the upstream web service
"""
from django.core.management.base import BaseCommand
import datetime
from odonto.models import Fp17IncompleteTreatment
from odonto import episode_categories
import dateutil.relativedelta as dr


class Command(BaseCommand):
    def handle(self, *args, **options):
        treatments = Fp17IncompleteTreatment.objects.filter(
            episode__stage="Submitted"
        )
        treatments = treatments.filter(
            episode__category_name=episode_categories.FP17Episode.display_name
        )
        treatments = treatments.exclude(completion_or_last_visit=None)

        three_mo = datetime.date.today() - dr.relativedelta(
            months=3
        )
        three_months_old = treatments.filter(
            completion_or_last_visit__lte=three_mo
        ).order_by("-completion_or_last_visit")
        print("Three months old")
        for i in three_months_old:
            print("{} {}".format(i.episode_id, i.completion_or_last_visit))

        nearly_three_months = treatments.exclude(
            completion_or_last_visit__lte=three_mo
        ).filter(
            completion_or_last_visit__lte=three_mo + datetime.timedelta(7)
        ).order_by("-completion_or_last_visit")
        print("Nearly three months")
        for i in nearly_three_months:
            print("{} {}".format(i.episode_id, i.completion_or_last_visit))
