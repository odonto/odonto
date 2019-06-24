from opal.core import episodes


class DentalCareEpisodeCategory(episodes.EpisodeCategory):
    display_name = "Dental Care"
    detail_template = "detail/dental_care.html"


class FP17Episode(episodes.EpisodeCategory):
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


class FP17OEpisode(episodes.EpisodeCategory):
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
            if not orthodontic_assessment.date_of_assessment:
                unsubmitted_fp7O_ids.append(episode.id)
            if not orthodontic_assessment.date_of_appliance_fitted:
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
