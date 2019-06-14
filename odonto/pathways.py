"""
Pathways for Odonto
"""
from django.db import transaction
from opal.core import menus, pathway
from odonto import models
from odonto.odonto_submissions import serializers


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
        return "/patient/{0}/".format(patient.id)


class AddPatientPathway(OdontoPagePathway):
    display_name = "Register Patient"
    slug = "add_patient"
    icon = "fa fa-user"

    steps = (
        models.Demographics,
    )

    @transaction.atomic
    def save(self, data, user=None, patient=None, episode=None):
        patient, episode = super().save(
            data, user=user, patient=patient, episode=episode
        )
        patient.create_episode(category_name='FP17', stage='New')
        patient.create_episode(category_name='FP17O', stage='New')
        return patient, episode


class EditDemographicsPathway(OdontoPagePathway):
    display_name = 'Edit Demographics'
    slug         = 'demographics'
    steps = [ models.Demographics ]


FP17_STEPS = (
    pathway.Step(
        model=models.Fp17DentalCareProvider,
        step_controller="CareProviderStepCtrl",
    ),
    pathway.Step(
        model=models.Demographics
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
        model=models.Fp17Declaration,
        display_name="Declaration",
        base_template="pathway/steps/declaration_base_template.html"
    ),
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


CHECK_STEP_FP17_O = pathway.Step(
    template="notused",
    base_template="pathway/steps/empty_step_base_template.html",
    step_controller="CheckFP17OStep",
    display_name="unused"
)


class SubmitFP17Pathway(OdontoPagePathway):
    display_name = 'Submit FP17'
    slug = 'fp17-submit'
    steps = FP17_STEPS + (CHECK_STEP_FP17,)
    template = "pathway/templates/check_pathway.html"
    summary_template = "partials/fp17_summary.html"

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
        model=models.Demographics
    ),
    pathway.Step(model=models.Fp17Exemptions),
    pathway.Step(
        model=models.OrthodonticDataSet
    ),
    pathway.Step(model=models.ExtractionChart),
    pathway.Step(model=models.OrthodonticAssessment),
    pathway.Step(model=models.OrthodonticTreatment),
    pathway.Step(
        model=models.Fp17Declaration,
        display_name="Declaration",
        base_template="pathway/steps/declaration_base_template.html"
    ),
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


class SubmitFP17OPathway(OdontoPagePathway):
    display_name = 'Submit FP17O'
    slug = 'fp17-o-submit'
    steps = FP17_O_STEPS + (CHECK_STEP_FP17_O,)
    template = "pathway/templates/check_pathway.html"
    summary_template = "partials/fp17_o_summary.html"

    @transaction.atomic
    def save(self, data, user=None, patient=None, episode=None):
        result = super().save(data, user, patient, episode)
        episode.stage = 'Submitted'
        episode.save()
        return result
