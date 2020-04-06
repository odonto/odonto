import datetime
from collections import defaultdict
from django.conf import settings
from opal.core import episodes


class DentalCareEpisodeCategory(episodes.EpisodeCategory):
    display_name = "Dental Care"
    detail_template = "detail/dental_care.html"


class AbstractOdontoCategory(object):
    SUBMITTED = "Submitted"
    OPEN = "Open"

    def submission(self):
        """
        It is possible that a submission could have been resent after
        an episode has successfully processed. This would be an
        error on our part but its logically possible.

        In that instance it would be rejected by compass even though
        the episode would have been successfully processed.

        To avoid this we return the submission that was successful if it
        exists.

        Otherwise we return the last rejection.
        """
        from odonto.odonto_submissions import models
        submissions = self.episode.submission_set.all()
        submissions = sorted(list(submissions), key=lambda x: x.created)
        successful_submission_states = [
            models.Submission.SUCCESS, models.Submission.MANUALLY_PROCESSED
        ]
        successful_submissions = [
            i for i in submissions if i.state in successful_submission_states
        ]
        if len(successful_submissions):
            return successful_submissions[-1]

        if submissions:
            return submissions[-1]

        return None

    @classmethod
    def get_successful_episodes(cls, qs=None):
        from opal.models import Episode
        from odonto.odonto_submissions import models

        successful_submission_states = [
            models.Submission.SUCCESS, models.Submission.MANUALLY_PROCESSED
        ]

        if qs is None:
            qs = Episode.objects.all()
        return (
            cls._get_submitted(qs)
            .filter(submission__state__in=successful_submission_states)
            .prefetch_related("submission_set")
        )

    @classmethod
    def get_rejected_episodes(cls, qs=None):
        from odonto.odonto_submissions import models

        qs = cls._get_submitted(qs)
        successful_ids = cls.get_successful_episodes(qs).values_list("id", flat=True)
        return (
            qs.exclude(id__in=successful_ids)
            .filter(submission__state=models.Submission.REJECTED_BY_COMPASS)
            .prefetch_related("submission_set")
        )

    @classmethod
    def _get_submitted(cls, qs=None):
        from opal.models import Episode

        if qs is None:
            qs = Episode.objects.all()
        return qs.filter(category_name=cls.display_name).filter(stage=cls.SUBMITTED)

    @classmethod
    def get_submitted_episodes(cls, qs=None):
        qs = cls._get_submitted(qs)
        return cls._get_submitted(qs).prefetch_related("submission_set")

    @classmethod
    def get_episodes_by_rejection(cls, qs=None):
        qs = cls._get_submitted(qs)
        reason_to_ids = defaultdict(list)
        rejected_episodes = cls.get_rejected_episodes(qs)

        for rejected_episode in rejected_episodes:
            reason = rejected_episode.category.submission().rejection
            reason_to_ids[reason].append(rejected_episode.id)

        result = {}

        for reason, episode_ids in reason_to_ids.items():
            result[reason] = qs.filter(id__in=episode_ids)

        return result

    @classmethod
    def get_oldest_unsent(cls, qs=None):
        unsent_date = datetime.datetime.max.date()
        unsent_episode = None
        for episode in qs:
            submission = episode.category.submission()
            if not submission or submission.state == submission.REJECTED_BY_COMPASS:
                sign_off_date = episode.category.get_sign_off_date()
                if sign_off_date and sign_off_date < unsent_date:
                    unsent_date = sign_off_date
                    unsent_episode = episode

        return unsent_episode

    @classmethod
    def summary(cls, qs=None):
        from opal.models import Episode

        if qs is None:
            qs = Episode.objects.all()
        qs = qs.filter(category_name=cls.display_name)
        result = defaultdict(int)
        start_of_today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        result["Sent today"] = qs.filter(submission__created__gte=start_of_today).count()
        result["Open"] = qs.filter(stage=cls.OPEN).count()
        result["Oldest unsent"] = None
        oldest_unsent = cls.get_oldest_unsent(qs)
        if oldest_unsent:
            result["Oldest unsent"] = oldest_unsent.category.get_sign_off_date()
        submitted_qs = cls._get_submitted(qs).prefetch_related("submission_set")

        for i in submitted_qs:
            submission = i.category.submission()

            if not submission:
                result["Submitted but not sent"] += 1
            else:
                if submission.state == submission.SENT:
                    result["Sent (result pending)"] += 1
                else:
                    result[submission.state] += 1
        # cast it to a dict so that we don't have the issue with calling .items
        # in a template (default dict returns .item rather than .items()
        # thus returning an int
        return dict(result)


class FP17Episode(episodes.EpisodeCategory, AbstractOdontoCategory):
    display_name = "FP17"
    detail_template = "n/a"

    def get_submit_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"{settings.HOST_NAME_AND_PROTOCOL}/pathway/#/fp17-submit/{patient_id}/{episode_id}"

    def get_edit_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"{settings.HOST_NAME_AND_PROTOCOL}/pathway/#/fp17-edit/{patient_id}/{episode_id}"

    @classmethod
    def get_unsubmitted(cls, qs):
        """
        Returns all unsubmitted fp17s
        fp17s are unsubmitted if they have a completion_or_last_visit
        """
        qs = qs.filter(stage="Open")
        return qs.filter(category_name="FP17").exclude(
            fp17incompletetreatment__completion_or_last_visit=None
        )

    def get_sign_off_date(self):
        """
        The date that we can consider this episode "done"
        """
        return self.episode.fp17incompletetreatment_set.all()[
            0
        ].completion_or_last_visit

    @classmethod
    def get_oldest_unsent(cls, qs=None):
        from opal.models import Episode

        if qs is None:
            qs = Episode.objects.all()
        qs = qs.filter(category_name=cls.display_name)
        qs = qs.prefetch_related("fp17incompletetreatment_set")
        return super().get_oldest_unsent(qs)


class FP17OEpisode(episodes.EpisodeCategory, AbstractOdontoCategory):
    display_name = "FP17O"
    detail_template = "n/a"

    def get_submit_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"{settings.HOST_NAME_AND_PROTOCOL}/pathway/#/fp17-o-submit/{patient_id}/{episode_id}"

    def get_edit_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"{settings.HOST_NAME_AND_PROTOCOL}/pathway/#/fp17-o-edit/{patient_id}/{episode_id}"

    @classmethod
    def get_unsubmitted(cls, qs):
        """
        fp17os are open if they have a date of assessment, a date of
        appliance or a date of completion
        """
        qs = qs.filter(stage="Open")
        fp17os = qs.filter(category_name="FP17O").prefetch_related(
            "orthodonticassessment_set", "orthodontictreatment_set"
        )
        unsubmitted_fp7O_ids = []
        for episode in fp17os:
            sign_off_date = episode.category.get_sign_off_date()
            if sign_off_date:
                unsubmitted_fp7O_ids.append(episode.id)
        return qs.filter(id__in=unsubmitted_fp7O_ids)

    def get_sign_off_date(self):
        """
        The date that we can consider this episode "done"

        Return the highest of
        orthodontic_assessment.date_of_assessment
        orthodontic_assessment.date_of_assessment
        orthodontic_treatment.date_of_completion
        """
        orthodontic_assessment = self.episode.orthodonticassessment_set.all()[0]
        orthodontic_treatment = self.episode.orthodontictreatment_set.all()[0]
        min_date = datetime.datetime.min.date()

        date_of_assessment = min_date

        if orthodontic_assessment.date_of_assessment:
            date_of_assessment = orthodontic_assessment.date_of_assessment

        date_of_appliance_fitted = min_date

        if orthodontic_assessment.date_of_appliance_fitted:
            date_of_appliance_fitted = orthodontic_assessment.date_of_appliance_fitted

        date_of_completion = min_date

        if orthodontic_treatment.date_of_completion:
            date_of_completion = orthodontic_treatment.date_of_completion

        largest_date = max(
            date_of_assessment, date_of_appliance_fitted, date_of_completion
        )

        if largest_date == min_date:
            return None

        return largest_date

    @classmethod
    def get_oldest_unsent(cls, qs=None):
        from opal.models import Episode

        if qs is None:
            qs = Episode.objects.all()
        qs = qs.filter(category_name=cls.display_name)
        qs = qs.prefetch_related(
            "orthodonticassessment_set", "orthodontictreatment_set"
        )
        return super().get_oldest_unsent(qs)


def get_unsubmitted_fp17_and_fp17os(qs):
    unsubmitted_fp17s = FP17Episode.get_unsubmitted(qs)
    unsubmitted_fp17Os = FP17OEpisode.get_unsubmitted(qs)
    return unsubmitted_fp17s | unsubmitted_fp17Os


def get_unsubmitted_fp17_and_fp17os_for_user(user):
    from opal.models import Episode

    qs = Episode.objects.all()
    for_user = get_episodes_for_user(qs, user)
    return get_unsubmitted_fp17_and_fp17os(for_user)


def get_episodes_for_user(qs, user):
    name = user.get_full_name()
    return qs.filter(fp17dentalcareprovider__performer=name)
