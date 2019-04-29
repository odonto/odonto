"""
Odonto views
"""
from django.views.generic import ListView

from opal.models import Episode

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
