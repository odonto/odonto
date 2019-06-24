from opal.core.api import LoginRequiredViewset
from opal.core import subrecords
from django.conf import settings
from django.utils.module_loading import import_string
from django.http import HttpResponseBadRequest
from opal.core.views import json_response


class DemographicsSearch(LoginRequiredViewset):
    base_name = 'demographics-search'
    PATIENT_FOUND_IN_APPLICATION = "patient_found_in_application"
    PATIENT_NOT_FOUND = "patient_not_found"

    def list(self, request, *args, **kwargs):
        Demographics = subrecords.get_subrecord_from_model_name("Demographics")
        nhs_number = request.query_params.get("nhs_number")
        if not nhs_number:
            return HttpResponseBadRequest("Please pass in an NHS number")
        demographics = Demographics.objects.filter(
            nhs_number=nhs_number
        ).last()

        # the patient is in odonto
        if demographics:
            return json_response(dict(
                patient=demographics.patient.to_dict(request.user),
                status=self.PATIENT_FOUND_IN_APPLICATION
            ))
        return json_response(dict(status=self.PATIENT_NOT_FOUND))
