"""
Odonto views
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from odonto import episode_categories

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
        qs = Episode.objects.filter(stage="Open")
        qs = episode_categories.get_episodes_for_user(
            qs, self.request.user
        )

        unsubmitted = episode_categories.get_unsubmitted_fp17_and_fp17os(qs)
        unsubmitted_ids = unsubmitted.values_list("id", flat=True)
        return qs.exclude(id__in=unsubmitted_ids)


class UnsubmittedFP17s(LoginRequiredMixin, TemplateView):
    template_name = "unsubmitted_list.html"

    def get_fp17s(self):
        qs = Episode.objects.all()
        qs = episode_categories.get_episodes_for_user(
            qs, self.request.user
        )
        return episode_categories.get_unsubmitted_fp17_and_fp17os_for_user(
            self.request.user
        )


class FP17SummaryDetailView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = 'fp17_summary.html'


class ViewFP17DetailView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = 'view_fp17.html'


class FP17OSummaryDetailView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = 'fp17_o_summary.html'


class ViewFP17ODetailView(LoginRequiredMixin, DetailView):
    model = Episode
    template_name = 'view_fp17_o.html'
