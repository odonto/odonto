"""
Gets the latest 'response' from which we can get the result of
submissions processed so far from Compass.

Then send an email with the current summary of the status quo so far.
"""
import traceback
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from opal.models import Episode

from odonto.odonto_submissions.models import (
    Response, Submission, EpisodesBeingInvestigated
)
from odonto.episode_categories import FP17Episode, FP17OEpisode, AbstractOdontoCategory
from odonto.odonto_submissions import logger
from odonto.utils import get_current_financial_year


class WarningField:
    """
    A class to flag that a field should be marked
    as needing a warning in the template
    """
    def __init__(self, value):
        self.value = value
        self.warning = True

    def __str__(self):
        return str(self.value)

    def __eq__(self, k):
        if not isinstance(k, WarningField):
            return False
        return self.value == k.value


def clean_episodes_being_investigated():
    """
    If an episode has been marked as in investigation
    and that episode has now succeeded
    """
    for instance in EpisodesBeingInvestigated.objects.all():
        episode = instance.episode
        if episode.category.submission().state == Submission.SUCCESS:
            logger.info(
                f"Investigated episode {episode.id} has successfully been sent"
            )
            instance.delete()


class Command(BaseCommand):
    def filter_by_tax_year(self, episodes):
        start_of_tax_year = get_current_financial_year()[0]
        episode_ids = set()
        for episode in episodes:
            sign_off_date = episode.category.get_sign_off_date()
            if sign_off_date and sign_off_date >= start_of_tax_year:
                episode_ids.add(episode.id)
        return episodes.filter(id__in=episode_ids)

    def get_oldest_rejection(self, qs):
        FAILURE_STATES = [
            Submission.FAILED_TO_SEND, Submission.REJECTED_BY_COMPASS
        ]
        rejected = qs.filter(submission__state__in=FAILURE_STATES)
        rejected_dates = [
            i.category.get_sign_off_date() for i in rejected if i.category.submission().state in FAILURE_STATES
        ]
        rejected_dates = [i for i in rejected_dates if i is not None]
        if len(rejected_dates) > 1:
            return min(rejected_dates)
        elif len(rejected_dates) == 1:
            return rejected_dates[0]
        else:
            return None


    def send_email(self, response):
        """
        Sends an email with a context dict where...

        title = the email subject.

        summary = a dictionary of dictionaries that will be put on the page. If
        it should be highlighted as a warning the result is cast to a WarningField
        """
        context = {"summary": {}}
        successful = response.get_successfull_submissions()
        rejected = Submission.objects.filter(
            id__in=[i.id for i in response.get_rejected_submissions().keys()]
        )

        fp17_category = FP17Episode.display_name
        fp17o_category = FP17OEpisode.display_name
        context["summary"]["Latest response"] = {
            "FP17 Success": successful.filter(episode__category_name=fp17_category).count(),
            "FP17 Rejected": rejected.filter(episode__category_name=fp17_category).count(),
            "FP17O Success": successful.filter(episode__category_name=fp17o_category).count(),
            "FP17O Rejected": rejected.filter(episode__category_name=fp17o_category).count(),
        }

        fp17_episodes_for_tax_year = self.filter_by_tax_year(Episode.objects.filter(category_name=FP17Episode.display_name))
        context["summary"]["FP17 current tax year"] = FP17Episode.summary(
            fp17_episodes_for_tax_year
        )
        error_states = [AbstractOdontoCategory.NEEDS_INVESTIGATION, Submission.REJECTED_BY_COMPASS]

        for error_state in error_states:
            if error_state in context["summary"]["FP17 current tax year"]:
                context["summary"]["FP17 current tax year"][error_state] = WarningField(
                    context["summary"]["FP17 current tax year"][error_state]
                )
        fp17O_episodes_for_tax_year = self.filter_by_tax_year(Episode.objects.filter(category_name=FP17OEpisode.display_name))
        context["summary"]["FP17O current tax year"] = FP17OEpisode.summary(
            fp17O_episodes_for_tax_year
        )
        for error_state in error_states:
            if error_state in context["summary"]["FP17O current tax year"]:
                context["summary"]["FP17O current tax year"][error_state] = WarningField(
                    context["summary"]["FP17O current tax year"][error_state]
                )
        context["summary"]["FP17 all time"] = FP17Episode.summary()
        context["summary"]["FP17O all time"] = FP17OEpisode.summary()
        today = datetime.date.today()
        oldest_fp17_date = self.get_oldest_rejection(fp17_episodes_for_tax_year) or datetime.datetime.max.date()
        oldest_fp17o_date = self.get_oldest_rejection(fp17O_episodes_for_tax_year) or datetime.datetime.max.date()
        old_rejection = min(oldest_fp17_date, oldest_fp17o_date)
        days_ago = today - old_rejection
        title = f"Odonto: Breaks need to be resolved in {60 - days_ago.days} day(s), NEEDS INVESTIGATION"
        context["title"] = title
        html_message = render_to_string("emails/response_summary.html", context)
        plain_message = strip_tags(html_message)
        admin_emails = ", ".join([i[1] for i in settings.ADMINS])
        logger.info(f"sending email {title} to {admin_emails}")
        send_mail(
            title,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            settings.ADMINS,
            html_message=html_message,
        )

    def has_current_tax_year_rejections_or_failed(self):
        """
        Returns True if we have episodes from the current tax year
        that have been rejected or failed to send.
        """
        failed_episodes = Episode.objects.filter(
            submission__state__in=[
                Submission.REJECTED_BY_COMPASS, Submission.FAILED_TO_SEND
            ]
        )
        if self.filter_by_tax_year(failed_episodes).exists():
            return True
        return False

    def handle(self, *args, **options):
        try:
            response = Response.get()
            response.update_submissions()
            if self.has_current_tax_year_rejections_or_failed():
                self.send_email(response)
            clean_episodes_being_investigated()
        except Exception as e:
            logger.info(f"Sending failed to get responses with {e}")
            logger.info(traceback.format_exc())
            logger.error('Failed to get responses')
