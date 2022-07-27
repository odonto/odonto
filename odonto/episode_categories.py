import datetime
from django.utils import timezone
from collections import defaultdict
from django.conf import settings
from opal.core import episodes


class DentalCareEpisodeCategory(episodes.EpisodeCategory):
    display_name = "Dental Care"
    detail_template = "detail/dental_care.html"


class AbstractOdontoCategory(object):
    detail_template = None
    NEW = "New"
    SUBMITTED = "Submitted"
    OPEN = "Open"
    NEW = "New"
    NEEDS_INVESTIGATION = "Not sent, needs investigation"

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
            submission = successful_submissions[-1]
            # if the latest submission is a delete, then return None
            if submission.submission_type == submission.DELETE:
                return None
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
            .prefetch_related("submission_set").distinct()
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
        from odonto.odonto_submissions.models import EpisodesBeingInvestigated

        if qs is None:
            qs = Episode.objects.all()
        qs = qs.filter(category_name=cls.display_name)
        result = defaultdict(int)
        start_of_today = timezone.make_aware(
            datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        )
        result["Open"] = qs.filter(stage=cls.OPEN).count()
        result["Oldest unsent"] = None
        oldest_unsent = cls.get_oldest_unsent(qs)
        if oldest_unsent:
            result["Oldest unsent"] = oldest_unsent.category.get_sign_off_date()
        submitted_qs = cls._get_submitted(qs).prefetch_related("submission_set")

        rejection_ignored = set(
            EpisodesBeingInvestigated.objects.all().values_list('episode_id', flat=True)
        )

        for i in submitted_qs:
            submission = i.category.submission()

            if not submission:
                # We should not have submissions sitting and waiting to send.
                # They should have been submitted by the send_submissions cron job
                # Therefore the most likely reason for no submission being sent down
                # is that the submission failed due to a flaw in the form
                # or that the patient has a protected address
                result[cls.NEEDS_INVESTIGATION] += 1
            else:
                if i.id in rejection_ignored:
                    if submission.state == submission.REJECTED_BY_COMPASS:
                        result["Rejected but ignored"] += 1
                elif submission.state == submission.SENT:
                    result["Sent (result pending)"] += 1
                else:
                    result[submission.state] += 1
        # cast it to a dict so that we don't have the issue with calling .items
        # in a template (default dict returns .item rather than .items()
        # thus returning an int
        return dict(result)


class FP17Episode(episodes.EpisodeCategory, AbstractOdontoCategory):
    display_name = "FP17"

    def get_submit_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"/pathway/#/fp17-submit/{patient_id}/{episode_id}"

    def get_edit_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"/pathway/#/fp17-edit/{patient_id}/{episode_id}"

    def get_summary_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"/#/summary/fp17/{patient_id}/{episode_id}"

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

    def uda(self):
        # as defined
        # https://contactcentreservices.nhsbsa.nhs.uk/selfnhsukokb/AskUs_Dental/en-gb/9737/units-of-activity-uda-uoa/41781/how-many-units-of-activity-uda-uoa-does-a-course-of-treatment-cot-receive
        # urgent treatment is band 4
        from odonto import models
        treatment_category = self.episode.fp17treatmentcategory_set.all()[0]
        treatment_map = {
            models.Fp17TreatmentCategory.BAND_1: 1,
            models.Fp17TreatmentCategory.BAND_2: 3,
            models.Fp17TreatmentCategory.BAND_3: 12,
            models.Fp17TreatmentCategory.URGENT_TREATMENT: 1.2,
            models.Fp17TreatmentCategory.REGULATION_11_REPLACEMENT_APPLIANCE: 12,
        }

        return treatment_map.get(treatment_category.treatment_category)


class FP17OEpisode(episodes.EpisodeCategory, AbstractOdontoCategory):
    display_name = "FP17O"

    def get_submit_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"/pathway/#/fp17-o-submit/{patient_id}/{episode_id}"

    def get_edit_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"/pathway/#/fp17-o-edit/{patient_id}/{episode_id}"

    def get_summary_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"/#/summary/fp17o/{patient_id}/{episode_id}"

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

    def uoa(self):
        from odonto import models
        # as defined
        # https://contactcentreservices.nhsbsa.nhs.uk/selfnhsukokb/AskUs_Dental/en-gb/9737/units-of-activity-uda-uoa/41781/how-many-units-of-activity-uda-uoa-does-a-course-of-treatment-cot-receive
        uoa = None
        assessment = self.episode.orthodonticassessment_set.all()[0]
        treatment = self.episode.orthodontictreatment_set.all()[0]

        if assessment.assessment == assessment.ASSESSMENT_AND_REVIEW:
            uoa = 1
        elif assessment.assessment == assessment.ASSESS_AND_REFUSE_TREATMENT:
            uoa = 1
        elif assessment.assessment == assessment.ASSESS_AND_APPLIANCE_FITTED:
            uoa = 1
            assessment_date = assessment.date_of_assessment
            demographics = models.Demographics.objects.filter(
                patient__episode=self.episode
            ).get()

            if not assessment_date:
                raise ValueError('date_of_assessment is required to calculate uoa')
            age = demographics.get_age(assessment_date)
            if age < 10:
                uoa += 3
            elif age < 18:
                uoa += 20
            else:
                uoa += 22

        if treatment.repair:
            if not uoa:
                uoa = 0
            uoa += 0.8

        if treatment.replacement and not uoa:
            uoa = 0

        return uoa


class CovidTriageEpisode(episodes.EpisodeCategory, AbstractOdontoCategory):
    display_name = "COVID-19 triage"

    def get_submit_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"/pathway/#/covid-triage-submit/{patient_id}/{episode_id}"

    def get_edit_link(self):
        patient_id = self.episode.patient_id
        episode_id = self.episode.id
        return f"/pathway/#/covid-triage-edit/{patient_id}/{episode_id}"

    @classmethod
    def get_unsubmitted(cls, qs):
        return qs.filter(
            category_name=cls.display_name
        ).filter(stage="Open")

    def get_sign_off_date(self):
        dt = self.episode.covidtriage_set.all()[0].datetime_of_contact
        if dt:
            return dt.date()


def get_unsubmitted_compass_episodes(qs):
    unsubmitted_fp17s = FP17Episode.get_unsubmitted(qs)
    unsubmitted_fp17Os = FP17OEpisode.get_unsubmitted(qs)
    unsubmitted_covid_triage = CovidTriageEpisode.get_unsubmitted(qs)
    return unsubmitted_fp17s | unsubmitted_fp17Os | unsubmitted_covid_triage


def get_unsubmitted_compass_episodes_for_user(user):
    from opal.models import Episode

    qs = Episode.objects.all()
    for_user = get_episodes_for_user(qs, user)
    return get_unsubmitted_compass_episodes(for_user)


def get_episodes_for_user(qs, user):
    name = user.get_full_name()
    return qs.filter(fp17dentalcareprovider__performer=name)
