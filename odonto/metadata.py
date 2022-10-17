"""
Inject metadata into Angular
"""
from opal.core.metadata import Metadata

from odonto.models import PerformerNumber, OtherDentalProfessional as OtherDentalProfessionalModel


class PerformerMetadata(Metadata):
    slug = 'performer'

    @classmethod
    def to_dict(klass, user=None, **kw):
        performer_list = [
            number.user.get_full_name() for number in
            PerformerNumber.objects.all().order_by('user__username')
        ]
        other_dcp_list = [
            other_professional.user.get_full_name() for other_professional in
            OtherDentalProfessionalModel.objects.all().order_by('user__username')
        ]
        current_user = None

        if user:
            if user.get_full_name() in performer_list:
                current_user = user.get_full_name()

        return {
            klass.slug: {
                'current_user': current_user,
                'performer_list': performer_list,
                'other_dcp_list': other_dcp_list
            }
        }
