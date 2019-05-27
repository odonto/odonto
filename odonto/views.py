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



class OpenFP17s(TemplateView):
    template_name = "open_list.html"

    def get_fp17s(self):
        name = self.request.user.get_full_name()
        qs = Episode.objects.filter(
            stage="Open",
            fp17dentalcareprovider__performer=name
        )
        episodes = []
        for e in qs:
            if e.category_name == 'FP17':
                if e.fp17incompletetreatment_set.get().completion_or_last_visit == None:
                    episodes.append(e)
            if e.category_name == 'FP17O':
                episodes.append(e)

        return episodes


class UnsubmittedFP17s(TemplateView):
    template_name = "unsubmitted_list.html"

    def get_fp17s(self):
        name = self.request.user.get_full_name()
        qs = Episode.objects.filter(
            stage="Open",
            fp17dentalcareprovider__performer=name
        )
        episodes = []
        for e in qs:
            if e.category_name == 'FP17':
                if e.fp17incompletetreatment_set.get().completion_or_last_visit:
                    episodes.append(e)
            if e.category_name == 'FP17O':
                episodes.append(e)

        return episodes


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
