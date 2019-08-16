angular.module('opal.services').factory('ExemptionsAndRemissionsValidator', function(){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessages}


  // if a patient has neither exemption fields
  // or a charge its an error.

  var EXEMPTION_FIELDS = [
    "patient_under_18",
    "full_remission_hc2_cert",
    "partial_remission_hc3_cert",
    "expectant_mother",
    "nursing_mother",
    "aged_18_in_full_time_education",
    "income_support",
    "nhs_tax_credit_exemption",
    "income_based_jobseekers_allowance",
    "pension_credit_guarantee_credit",
    "prisoner",
    "universal_credit",
    "income_related_employment_and_support_allowance",
    "evidence_of_exception_or_remission_seen",
  ]

  var FREE_TREATMENTS = [
    "prescription_only",
    "denture_repairs",
    "bridge_repairs",
    "arrest_of_bleeding",
    "removal_of_sutures"
  ]

  var exceptionOrCharge = function(editing){
    if(!editing.fp17_exemptions.patient_charge_collected){
      var exemptionSelected = _.some(EXEMPTION_FIELDS, function(exemptionField){
        return editing.fp17_exemptions[exemptionField]
      })

      if(!exemptionSelected){
        return true;
      }
    }
  }


  /*
  These treatments don't require payment. This may not be _exactly_ correct
  as its plausible that the patient has other treatments _aswell_ as these
  however we are going back to the dentists for clarification.
  */
  var freeTreatments = function(editing){
    var result = _.find(FREE_TREATMENTS, function(ft){
      return editing.fp17_treatment_category[ft];
    });

    return result;
  }

  return function(editing) {
    if(exceptionOrCharge(editing) && !freeTreatments(editing)){
      return {
        fp17_exemptions: {
          step_error: "Please select an exemption or add the charge"
        }
      }
    }
  }
});
