"""
Odonto views
"""
from django.views.generic import ListView, DetailView

from opal.models import Episode, Patient

from odonto.utils import has_open_fp17, has_open_fp17o

class UnsubmittedFP17s(ListView):
    model = Episode
    paginate_by = 50

    def get_queryset(self, *a, **k):
        name = self.request.user.get_full_name()
        qs = self.model.objects.filter(
            stage="Open",
            fp17incompletetreatment__completion_or_last_visit__isnull=False,
            fp17dentalcareprovider__performer=name
        )
        return qs


class PatientDetailView(DetailView):
    model = Patient

    def get_context_data(self, **k):
        """
        Add additional context variables to the patient
        detail view.
        """
        context = super().get_context_data(**k)
        patient = self.get_object()

        context['open_fp17']  = has_open_fp17(patient)
        context['open_fp17o'] = has_open_fp17o(patient)
        return context
