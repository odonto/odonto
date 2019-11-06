from collections import defaultdict
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
        successful_submissions = [
            i for i in submissions if i.state == models.Submission.SUCCESS
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

        if qs is None:
            qs = Episode.objects.all()
        return cls._get_submitted(qs).filter(
            submission__state=models.Submission.SUCCESS
        ).prefetch_related("submission_set")

    @classmethod
    def get_rejected_episodes(cls, qs=None):
        from odonto.odonto_submissions import models
        qs = cls._get_submitted(qs)
        successful_ids = cls.get_successful_episodes(qs).values_list(
            "id", flat=True
        )
        return qs.exclude(
            id__in=successful_ids
        ).filter(
            submission__state=models.Submission.REJECTED_BY_COMPASS
        ).prefetch_related("submission_set")

    @classmethod
    def _get_submitted(cls, qs):
        from opal.models import Episode
        if qs is None:
            qs = Episode.objects.all()
        return qs.filter(category_name=cls.display_name).filter(
            stage=cls.SUBMITTED
        )

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


class FP17Episode(episodes.EpisodeCategory, AbstractOdontoCategory):
    display_name = 'FP17'
    detail_template = 'n/a'

    @classmethod
    def get_unsubmitted(cls, qs):
        """
        Returns all unsubmitted fp17s
        fp17s are unsubmitted if they have a completion_or_last_visit_date
        """
        qs = qs.filter(stage="Open")
        return qs.filter(
            category_name="FP17"
        ).exclude(
            fp17incompletetreatment__completion_or_last_visit=None
        )


class FP17OEpisode(episodes.EpisodeCategory, AbstractOdontoCategory):
    display_name = 'FP17O'
    detail_template = 'n/a'

    @classmethod
    def get_unsubmitted(cls, qs):
        """
        fp17os are open if they have a date of assessment, a date of
        appliance or a date of completion
        """
        qs = qs.filter(stage="Open")
        fp17os = qs.filter(
            category_name="FP17O"
        ).prefetch_related(
            "orthodonticassessment_set", "orthodontictreatment_set"
        )
        unsubmitted_fp7O_ids = []
        for episode in fp17os:
            orthodontic_assessment = episode.orthodonticassessment_set.all()[0]
            if orthodontic_assessment.date_of_assessment:
                unsubmitted_fp7O_ids.append(episode.id)
            if orthodontic_assessment.date_of_appliance_fitted:
                unsubmitted_fp7O_ids.append(episode.id)
            orthodontic_treatment = episode.orthodontictreatment_set.all()[0]
            if orthodontic_treatment.date_of_completion:
                unsubmitted_fp7O_ids.append(episode.id)
        return qs.filter(id__in=unsubmitted_fp7O_ids)


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
    return qs.filter(
        fp17dentalcareprovider__performer=name
    )
