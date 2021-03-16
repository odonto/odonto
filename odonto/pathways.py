"""
Pathways for Odonto
"""
import logging
from django.db import transaction
from opal.core import pathway
from odonto import models
from odonto.odonto_submissions import models as submission_models
from odonto.episode_categories import (
    FP17Episode, FP17OEpisode, CovidTriageEpisode
)
from plugins.add_patient_step import FindPatientStep


def is_submitted(episode):
    failed = [
        submission_models.Submission.FAILED_TO_SEND,
        submission_models.Submission.REJECTED_BY_COMPASS,
    ]
    return episode.submission_set.exclude(
        state__in=failed
    ).exists()


class OdontoPagePathway(pathway.PagePathway):
    @classmethod
    def get_absolute_url(klass, **kwargs):
        base = '/pathway/#/{0}/'.format(klass.slug)

        if any(('patient' in kwargs, 'ngpatient' in kwargs)):
            if 'patient' in kwargs:
                target = base + '{0}/'.format(kwargs['patient'].id)
            else:
                target = base + '[[ {0} ]]/'.format(kwargs['ngpatient'])

            if any(('episode' in kwargs, 'ngepisode' in kwargs)):
                if 'episode' in kwargs:
                    target = target + '{0}/'.format(kwargs['episode'].id)
                else:
                    target = target + '[[ {0} ]]/'.format(kwargs['ngepisode'])
            return target

        else:
            return base

    def redirect_url(self, user=None, patient=None, episode=None):
        return patient.get_absolute_url()


class AddPatientPathway(OdontoPagePathway):
    display_name = "Register patient"
    slug = "add_patient"
    icon = "fa fa-user"
    template = "pathway/templates/add_patient_base.html"
    finish_button_text = "Register patient"

    steps = (
        FindPatientStep(
            base_template="pathway/steps/step_base_without_display_name.html"
        ),
    )

    @transaction.atomic
    def save(self, data, user=None, patient=None, episode=None):
        patient, episode = super().save(
            data, user=user, patient=patient, episode=episode
        )
        patient.create_episode(
            category_name=FP17Episode.display_name, stage='New'
        )
        patient.create_episode(
            category_name=FP17OEpisode.display_name, stage='New'
        )
        patient.create_episode(
            category_name=CovidTriageEpisode.display_name, stage='New'
        )
        demographics = patient.demographics()
        if models.Demographics.objects.filter(
            first_name=demographics.first_name,
            surname=demographics.surname,
            date_of_birth=demographics.date_of_birth
        ).count() > 2:
            err = "A patient has been saved but another already exists with the \
same name and DOB"
            logging.error(err)
        return patient, episode


FP17_STEPS = (
    pathway.Step(
        model=models.Fp17DentalCareProvider,
        step_controller="CareProviderStepCtrl",
    ),
    pathway.Step(
        model=models.Demographics,
        base_template="pathway/steps/step_base_without_display_name.html"
    ),
    pathway.Step(
        model=models.Fp17IncompleteTreatment,
        step_controller="FP17TreatmentStepCtrl",
    ),
    pathway.Step(model=models.Fp17Exemptions),
    pathway.Step(model=models.Fp17ClinicalDataSet),
    pathway.Step(model=models.Fp17OtherDentalServices),
    pathway.Step(model=models.Fp17TreatmentCategory),
    pathway.Step(model=models.Fp17Recall),
    pathway.Step(
        model=models.CovidStatus,
        help_template="pathway/covid_status_help.html"
    ),
    pathway.Step(model=models.CaseMix, help_template="pathway/case_mix_help.html"),
)


class Fp17Pathway(OdontoPagePathway):
    display_name = 'Open FP17'
    slug = 'fp17'
    steps = FP17_STEPS

    @transaction.atomic
    def save(self, data, user=None, patient=None, episode=None):
        patient, episode = super().save(
            data, user=user, patient=patient, episode=episode
        )
        episode.stage = 'Open'
        episode.save()
        patient.create_episode(category_name='FP17', stage='New')
        return patient, episode


CHECK_STEP_FP17 = pathway.Step(
    template="notused",
    base_template="pathway/steps/empty_step_base_template.html",
    step_controller="CheckFP17Step",
    display_name="unused"
)


class SubmitFP17Pathway(OdontoPagePathway):
    display_name = 'Submit FP17'
    slug = 'fp17-submit'
    steps = FP17_STEPS + (CHECK_STEP_FP17,)
    template = "pathway/templates/check_pathway.html"
    summary_template = "partials/fp17_summary.html"

    def get_overlapping_dates(self, patient, episode):
        """
        For date of acceptance and date of completion or last_visit
        we care about whether there are overlapping episodes.

        overlapping episodes are all episodes that are not
        Urgent treatment/denture repaires/bridge repairs.

        We care if our date of acceptance is between another episodes
        date of acceptance and date of completion or whether our date of
        acceptance is between another date of completion.

        Return [date_of_acceptance, date_of_completion_or_last_visit]
        date_of_completion_or_last_visit may be None.
        """
        result = patient.episode_set.filter(
            category_name=FP17Episode.display_name
        ).exclude(
            id=episode.id
        ).exclude(
            fp17treatmentcategory__treatment_category__in=[
                models.Fp17TreatmentCategory.URGENT_TREATMENT,
                models.Fp17TreatmentCategory.DENTURE_REPAIRS,
                models.Fp17TreatmentCategory.BRIDGE_REPAIRS,
            ]
        ).values_list(
            'fp17incompletetreatment__date_of_acceptance',
            'fp17incompletetreatment__completion_or_last_visit'
        )
        return [i for i in result if i[0]]

    def get_further_treatment_information(self, patient, episode):
        """
        If ‘Further treatment within 2 months’ is present then the same provider
        must have a claim(s) for this patient in the two months prior to the acceptance
        date of the continuation claim. There must be at least one instance of a valid
        claim in the two month period.  Valid claims exclude urgent (9150 4), incomplete (9164),
        Further treatment within 2 months (9163) or a lower band.

        return [{treatment_category: date_of_acceptance}]
        """
        category_and_acceptance = patient.episode_set.filter(
            category_name=FP17Episode.display_name
        ).exclude(
            id=episode.id
        ).filter(
            stage=FP17Episode.SUBMITTED
        ).exclude(
            fp17treatmentcategory__treatment_category=models.Fp17TreatmentCategory.URGENT_TREATMENT
        ).filter(
            fp17incompletetreatment__incomplete_treatment=None
        ).filter(
            fp17otherdentalservices__further_treatment_within_2_months=False
        ).values(
            "fp17treatmentcategory__treatment_category", "fp17incompletetreatment__date_of_acceptance"
        )

        result = []
        for i in category_and_acceptance:
            if i["fp17incompletetreatment__date_of_acceptance"]:
                result.append({
                    "category": i["fp17treatmentcategory__treatment_category"],
                    "date_of_acceptance": i["fp17incompletetreatment__date_of_acceptance"]
                })

        return result

    def to_dict(self, *args, **kwargs):
        patient = kwargs.get('patient')
        episode = kwargs.get('episode')
        to_dicted = super().to_dict(*args, **kwargs)

        check_index = None
        for index, step_dict in enumerate(to_dicted["steps"]):
            if step_dict["step_controller"] == CHECK_STEP_FP17.get_step_controller():
                check_index = index

        overlapping_dates = self.get_overlapping_dates(patient, episode)
        to_dicted["steps"][check_index]["overlapping_dates"] = overlapping_dates
        further_treatment_information = self.get_further_treatment_information(patient, episode)
        to_dicted["steps"][check_index]["further_treatment_information"] = further_treatment_information
        to_dicted["steps"][check_index]["episode_submitted"] = is_submitted(episode)
        return to_dicted

    @transaction.atomic
    def save(self, data, user=None, patient=None, episode=None):
        result = super().save(data, user, patient, episode)
        episode.stage = 'Submitted'
        episode.save()
        return result


class EditFP17Pathway(OdontoPagePathway):
    display_name = 'Edit FP17'
    slug = 'fp17-edit'
    steps = FP17_STEPS


FP17_O_STEPS = (
    pathway.Step(
        model=models.Fp17DentalCareProvider,
        step_controller="CareProviderStepCtrl",
    ),
    pathway.Step(
        model=models.Demographics,
        base_template="pathway/steps/step_base_without_display_name.html"
    ),
    pathway.Step(model=models.Fp17Exemptions),
    pathway.Step(
        model=models.OrthodonticDataSet
    ),
    pathway.Step(model=models.ExtractionChart),
    pathway.Step(model=models.OrthodonticAssessment),
    pathway.Step(model=models.OrthodonticTreatment),
    pathway.Step(
        model=models.CovidStatus,
        help_template="pathway/covid_status_help.html"
    ),
    pathway.Step(model=models.CaseMix, help_template="pathway/case_mix_help.html"),
)


class Fp17OPathway(OdontoPagePathway):
    display_name = 'FP17O claim form'
    slug = 'fp17o'
    steps = FP17_O_STEPS

    @transaction.atomic
    def save(self, data, user=None, patient=None, episode=None):
        patient, episode = super().save(
            data, user=user, patient=patient, episode=episode
        )
        episode.stage = 'Open'
        episode.save()
        patient.create_episode(category_name='FP17O', stage='New')
        return patient, episode


class EditFP17OPathway(OdontoPagePathway):
    display_name = 'Edit FP17O'
    slug = 'fp17-o-edit'
    steps = FP17_O_STEPS


CHECK_STEP_FP17_O = pathway.Step(
    template="notused",
    base_template="pathway/steps/empty_step_base_template.html",
    step_controller="CheckFP17OStep",
    display_name="unused"
)


class SubmitFP17OPathway(OdontoPagePathway):
    display_name = 'Submit FP17O'
    slug = 'fp17-o-submit'
    steps = FP17_O_STEPS + (CHECK_STEP_FP17_O,)
    template = "pathway/templates/check_pathway.html"
    summary_template = "partials/fp17_o_summary.html"

    def get_overlapping_dates(self, patient, episode):
        """
        If a patient has:
            episode one with:
                date of assessment on Monday
                date of appliance fitted on Friday
            episode two with:
                date of completion on Tuesday

        Then we expect a validation warning to appear on both episodes.

        This adds the dates of other episodes so we can raise this error.

        Note date of referral does not seem to be relevent based on the
        existing cases submitted errors/responses.

        If the previous episode and the current episode have a
        completion type then we reject it as an assessment epsode type is
        expected first. To test for this we serialize episode
        types with their related dates.
        """
        result = []
        other_episodes = patient.episode_set.exclude(
            id=episode.id, category_name=FP17OEpisode.display_name
        )
        for episode in other_episodes:
            assessment = episode.orthodonticassessment_set.all()[0]
            completion = episode.orthodontictreatment_set.all()[0]
            date_of_assessment = assessment.date_of_assessment
            date_of_appliance_fitted = assessment.date_of_appliance_fitted
            date_of_completion = completion.date_of_completion
            dts = [i for i in [date_of_assessment, date_of_appliance_fitted, date_of_completion] if i]
            if dts:
                if len(dts) > 2:
                    dates = [min(dts), max(dts)]
                else:
                    dates = sorted(dts)
                result.append({
                    "dates": dates,
                    "completion_type": completion.completion_type
                })
        return result

    def to_dict(self, *args, **kwargs):
        patient = kwargs.get('patient')
        episode = kwargs.get('episode')
        to_dicted = super().to_dict(*args, **kwargs)
        check_index = None
        for index, step_dict in enumerate(to_dicted["steps"]):
            if step_dict["step_controller"] == CHECK_STEP_FP17_O.get_step_controller():
                check_index = index

        to_dicted["steps"][check_index]
        overlapping_dates = self.get_overlapping_dates(patient, episode)
        to_dicted["steps"][check_index]["overlapping_dates"] = overlapping_dates
        to_dicted["steps"][check_index]["episode_submitted"] = is_submitted(episode)
        return to_dicted

    @transaction.atomic
    def save(self, data, user=None, patient=None, episode=None):
        result = super().save(data, user, patient, episode)
        episode.stage = 'Submitted'
        episode.save()
        return result


# Covid triage
COVID_TRIAGE_STEPS = (
    pathway.Step(
        model=models.Fp17DentalCareProvider,
        step_controller="CareProviderStepCtrl",
    ),
    pathway.Step(
        model=models.Demographics,
        base_template="pathway/steps/step_base_without_display_name.html"
    ),
    pathway.Step(
        model=models.CovidTriage,
        base_template="pathway/steps/step_base_without_display_name.html",
        step_controller="CovidTriageStepCtrl"
    ),
)


class CovidTriagePathway(OdontoPagePathway):
    display_name = 'Covid triage claim form'
    slug = 'covid-triage-new'
    steps = COVID_TRIAGE_STEPS

    @transaction.atomic
    def save(self, data, user=None, patient=None, episode=None):
        patient, episode = super().save(
            data, user=user, patient=patient, episode=episode
        )
        episode.stage = 'Open'
        episode.save()
        patient.create_episode(
            category_name=CovidTriageEpisode.display_name,
            stage=CovidTriageEpisode.NEW
        )
        return patient, episode


class EditCovidTriagePathway(OdontoPagePathway):
    display_name = 'Edit triage'
    slug = 'covid-triage-edit'
    steps = COVID_TRIAGE_STEPS


class SubmitCovidTriagePathway(OdontoPagePathway):
    display_name = "Submit triage"
    slug = 'covid-triage-submit'
    steps = COVID_TRIAGE_STEPS

    @transaction.atomic
    def save(self, data, user=None, patient=None, episode=None):
        result = super().save(data, user, patient, episode)
        episode.stage = 'Submitted'
        episode.save()
        return result

