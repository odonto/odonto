from opal.core.pathway import Step
from django.urls import reverse_lazy


class FindPatientStep(Step):
    template = "add_patient/pathway/find_patient_form.html"
    step_controller = "LookupPatientCrl"
    display_name = "Find patient"
    icon = "fa fa-user"

    # an end point that takes a get parameter of nhs_number
    search_end_point = reverse_lazy("demographics-search-list")

    def to_dict(self, *args, **kwargs):
        dicted = super().to_dict(*args, **kwargs)
        dicted["search_end_point"] = str(self.search_end_point)
        return dicted
