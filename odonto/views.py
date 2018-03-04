"""
Views for the Odonto application
"""
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from opal.models import Patient

from odonto import pathways


class CreateNewEpidsodeForFP17View(View):
    """
    When we GET this URL, create a new episode
    for the patient in question and redirect to the new FP17 form
    for that episode.
    """
    # TODO: This entire thing is probably not a good idea. Rethink it.
    def get(self, request, **kwargs):
        patient = get_object_or_404(Patient, pk=kwargs['pk'])
        episode = patient.create_episode()
        return redirect(pathways.Fp17Pathway.get_absolute_url(
            patient=patient, episode=episode))
