"""
odonto - Our Opal Application
"""
from opal.core import application, menus
from odonto import episode_categories


class Application(application.OpalApplication):
    default_episode_category = episode_categories.DentalCareEpisodeCategory.display_name

    javascripts = [
        'js/openodonto/routes.js',
        'js/openodonto/controllers/careprovider.step.controller.js',
        'js/openodonto/controllers/covid_triage.step.controller.js',
        'js/openodonto/controllers/fp17treatment.step.controller.js',
        'js/openodonto/controllers/complete_fp17_other_dental_services.controller.step.js',
        'js/openodonto/controllers/check_fp17.step.controller.js',
        'js/openodonto/controllers/check_fp17_o.step.controller.js',
        'js/openodonto/controllers/check_covid_triage.step.controller.js',
        'js/openodonto/controllers/summary.controller.js',
        'js/openodonto/controllers/dental_care.controller.js',
        'js/openodonto/controllers/casemix_helper.controller.js',
        'js/openodonto/controllers/delete_form.controller.js',
        'js/openodonto/services/date_conflict_check.js',
        'js/openodonto/services/validators/exemptions_and_remissions.js',
        'js/openodonto/services/validators/case_mix_required.js',
        'js/openodonto/services/validators/provider_location_number_required.js',
        'js/openodonto/services/validators/fp17_completion_or_last_visit.js',
        'js/openodonto/services/validators/form_validation.js',
        'js/openodonto/services/validators/nhs_number_validator.js',
        'js/openodonto/services/validators/date_of_birth_required.js',
        'js/openodonto/services/validators/address_required.js',
        'js/openodonto/services/validators/appliance_greater_than_assessment.js',
        'js/openodonto/services/validators/fp17_date_of_acceptance.js',
        'js/openodonto/services/validators/fp17_further_treatment.js',
        'js/openodonto/services/validators/fp17o_under_18.js',
        'js/openodonto/services/validators/fp17_under_18.js',
        'js/openodonto/services/validators/fp17_male_mother.js',
        'js/openodonto/services/validators/fp17_free_repair_replacement.js',
        'js/openodonto/services/validators/fp17o_commissioner_approval.js',
        'js/openodonto/services/validators/fp17o_date_of_referral.js',
        'js/openodonto/services/validators/fp17o_date_of_assessment.js',
        'js/openodonto/services/validators/fp17o_date_of_appliance_fitted.js',
        'js/openodonto/services/validators/fp17o_assessment_type.js',
        'js/openodonto/services/validators/fp17o_assessment_iotn.js',
        'js/openodonto/services/validators/fp17o_phone_number_required.js',
        'js/openodonto/services/validators/fp17o_email_required.js',
        'js/openodonto/services/validators/fp17o_regulation_11.js',
        'js/openodonto/services/validators/fp17o_assessment_aesthetic_component.js',
        'js/openodonto/services/validators/fp17o_treatment_iotn.js',
        'js/openodonto/services/validators/fp17_treatment_category.js',
        'js/openodonto/services/validators/fp17o_treatment_aesthetic_component.js',
        'js/openodonto/services/validators/fp17o_date_of_completion.js',
        'js/openodonto/services/validators/fp17_aged_18_full_time_education.js',
        'js/openodonto/services/validators/fp17o_aged_18_full_time_education.js',
        'js/openodonto/services/validators/fp17o_completion_type.js',
        'js/openodonto/services/validators/covid_triage_covid_status_required.js',
        'js/openodonto/services/validators/covid_triage_datetime_of_contact.js',
        'js/openodonto/services/validators/covid_triage_primary_reason_required.js',
        'js/openodonto/services/validators/covid_triage_type_required.js',
    ]
