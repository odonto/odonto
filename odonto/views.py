"""
Odonto views
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView

from opal.models import Episode, Patient


def has_open_fp17(patient):
    return patient.episode_set.filter(
        category_name='FP17').exclude(
            stage__in=['New', 'Submitted']).exists()


def has_open_fp17o(patient):
    return patient.episode_set.filter(
        category_name='FP17O').exclude(
            stage__in=['New', 'Submitted']).exists()


def get_submitted_forms(qs):
    """
    Takes in a qs of episodes
    Returns a list of episodes that have an
    unsubmitted fp17 or fp17O
    """

    # fp17s are open if they have a completion_or_last_visit_date
    qs = qs.filter(stage="Open")
    unsubmitted_fp17_ids = list(qs.filter(
        category_name="FP17"
    ).exclude(
        fp17incompletetreatment__completion_or_last_visit=None
    ).values_list("id", flat=True))

    fp17os = qs.filter(
        category_name="FP17O"
    ).prefetch_related("orthodonticassessment_set", "orthodontictreatment_set")
    unsubmitted_fp7O_ids = []

    # fp17s are open if they have a date of assessment or a date of appliance
    # or a date of completion
    for episode in fp17os:
        orthodontic_assessment = episode.orthodonticassessment_set.all()[0]
        if not orthodontic_assessment.date_of_assessment:
            unsubmitted_fp7O_ids.append(episode.id)
        if not orthodontic_assessment.date_of_appliance_fitted:
            unsubmitted_fp7O_ids.append(episode.id)
        orthodontic_treatment = episode.orthodontictreatment_set.all()[0]
        if orthodontic_treatment.date_of_completion:
            unsubmitted_fp7O_ids.append(episode.id)
    unsubmitted_ids = unsubmitted_fp17_ids + unsubmitted_fp7O_ids
    return qs.filter(id__in=unsubmitted_ids)


class OpenFP17s(TemplateView):
    template_name = "open_list.html"

    def get_fp17s(self):
        name = self.request.user.get_full_name()
        qs = Episode.objects.filter(
            fp17dentalcareprovider__performer=name
        )
        unsubmitted_ids = get_submitted_forms(qs).values_list("id", flat=True)

        return qs.exclude(
            id__in=unsubmitted_ids
        )


class UnsubmittedFP17s(TemplateView):
    template_name = "unsubmitted_list.html"

    def get_fp17s(self):
        name = self.request.user.get_full_name()
        qs = Episode.objects.filter(
            fp17dentalcareprovider__performer=name
        )
        return get_submitted_forms(qs)


class PatientDetailView(DetailView):
    model = Patient

    def get_context_data(self, **k):
        """
        Add additional context variables to the patient
        detail view.
        """
        context = super().get_context_data(**k)
        patient = self.get_object()
        episodes = patient.episode_set.filter(category_name__in=['FP17', 'FP17O'])

        context['episodes']   = episodes
        context['open_fp17']  = has_open_fp17(patient)
        context['open_fp17o'] = has_open_fp17o(patient)

        context['new_fp17_pk']  = patient.episode_set.get(category_name='FP17', stage='New').pk
        context['new_fp17o_pk'] = patient.episode_set.get(category_name='FP17O', stage='New').pk

        return context


class SubmitFP17DetailView(DetailView):
    model = Episode
    template_name = 'submit_fp17.html'

    def post(self, request, *args, **kwargs):
        # Validation ?
        episode = self.get_object()
        episode.stage = 'Submitted'
        episode.save()
        return redirect(reverse('odonto-patient-detail', args=[episode.patient.pk]))


class ViewFP17DetailView(DetailView):

    model = Episode
    template_name = 'view_fp17.html'




class SubmitFP17ODetailView(DetailView):
    model = Episode
    template_name = 'submit_fp17_o.html'

    def post(self, request, *args, **kwargs):
        # Validation ?
        episode = self.get_object()
        episode.stage = 'Submitted'
        episode.save()
        return redirect(reverse('odonto-patient-detail', args=[episode.patient.pk]))


class ViewFP17ODetailView(DetailView):

    model = Episode
    template_name = 'view_fp17_o.html'
