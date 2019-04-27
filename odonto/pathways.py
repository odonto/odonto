"""
Pathways for Odonto
"""
from opal.core import menus, pathway
from odonto import models
from odonto.odonto_submissions import serializers


class PathwayUrlMixin(object):

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


class AsMenuItemMixin(object):

    @classmethod
    def as_menuitem(cls, **kwargs):
        """
        Return an Opal MenuItem for this Pathway.

        Uses the following defaults, any of which may be overridden
        as kwargs:

        * `href`: .get_absolute_url()
        * `activepattern` : .get_absolute_url()
        * `icon`: .icon
        * `display`: .display_name
        """
        menuitem_kwargs = {}

        if 'href' in kwargs:
            menuitem_kwargs['href'] = kwargs['href']
        else:
            menuitem_kwargs['href'] = cls.get_absolute_url()

        if 'activepattern' in kwargs:
            menuitem_kwargs['activepattern'] = kwargs['activepattern']
        else:
            menuitem_kwargs['activepattern'] = cls.get_absolute_url()

        if 'icon' in kwargs:
            menuitem_kwargs['icon'] = kwargs['icon']
        else:
            menuitem_kwargs['icon'] = cls.icon

        if 'display' in kwargs:
            menuitem_kwargs['display'] = kwargs['display']
        else:
            menuitem_kwargs['display'] = cls.display_name

        return menus.MenuItem(**menuitem_kwargs)


class OdontoPagePathway(PathwayUrlMixin, AsMenuItemMixin, pathway.PagePathway):
    pass


class AddPatientPathway(OdontoPagePathway):
    display_name = "Add Patient"
    slug = "add_patient"
    icon = "fa fa-user"

    steps = (
        models.Demographics,
    )

    def save(self, data, user=None, patient=None, episode=None):
        patient, episode = super().save(
            data, user=user, patient=patient, episode=episode
        )
        episode.stage = 'New'
        episode.save()
        return patient, episode

    def redirect_url(self, user=None, patient=None, episode=None):
        return "/#/patient/{0}/".format(patient.id)


class Fp17Pathway(OdontoPagePathway):
    display_name = 'FP17 claim form'
    slug = 'fp17'
    steps = (
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

    def save(self, data, user=None, patient=None, episode=None):
        patient, episode = super().save(
            data, user=user, patient=patient, episode=episode
        )
        episode.stage = 'Open'
        episode.save()
        return patient, episode


class CompleteFP17Pathway(Fp17Pathway):
    display_name = "Submit FP17"
    slug         = "complete-fp17"
    finish_button_text = "Submit to BSA"

    def save(self, data, user=None, patient=None, episode=None):
        patient, episode = super().save(
            data, user=user, patient=patient, episode=episode
        )
        episode.stage = 'Submitted'
        episode.save()
        patient.create_episode(stage="New")
        serializer = serializers.FP17Serializer(episode, user)
        serializer.save()
        return patient, episode


class Fp17OPathway(OdontoPagePathway):
    display_name = 'FP17O claim form'
    slug = 'fp17o'
    steps = (
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
        pathway.Step(model=models.OrthodonticAssessment),
        pathway.Step(model=models.OrthodonticTreatment),
        pathway.Step(
            model=models.Fp17Declaration,
            display_name="Declaration",
            base_template="pathway/steps/declaration_base_template.html"
        ),
    )

    def save(self, data, user=None, patient=None, episode=None):
        patient, episode = super().save(
            data, user=user, patient=patient, episode=episode
        )
        episode.stage = 'Open'
        episode.save()
        return patient, episode
