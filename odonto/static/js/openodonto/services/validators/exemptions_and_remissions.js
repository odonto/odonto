angular.module('opal.services').factory('ExemptionsAndRemissionsValidator', function(ValidatorUtils){
  "use strict";
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessages}


  // if a patient has neither exemption fields
  // or a charge its an error.
  var exceptionOrCharge = function(editing){
    /*
    * returns an error message if the form is invalid
    */
    if(editing.fp17_other_dental_services.free_repair_or_replacement){
      return;
    }

    if(!editing.fp17_exemptions.patient_charge_collected){
      if(!ValidatorUtils.hasExemption(editing)){
        if(editing.fp17_exemptions.partial_remission_hc3_cert){
          return "A charge is required if there is only a partial exemption";
        }
        return "Please select an exemption or add the charge";
      }
    }
  }

  return function(editing) {
    var err = exceptionOrCharge(editing);
    if(err){
      return {
        fp17_exemptions: {
          step_error: err
        }
      }
    }

  }
});
