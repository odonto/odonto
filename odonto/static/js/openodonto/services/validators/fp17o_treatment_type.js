angular.module('opal.services').factory('Fp17OTreatmentType', function(){
  /*
  * from an email in feb 2020,
  * Proposed Treatment mandatory on Assess/Appliance Fitted claims
  */
  return function(editing){
    "use strict";
    var assessmentReason = editing.orthodontic_assessment.assessment;
    var treatmentType = editing.orthodontic_data_set.treatment_type;
    var ASSESS_AND_APPLIANCE_FITTED = "Assess & appliance fitted"
    var PROPOSED = "Proposed"

    if(assessmentReason === ASSESS_AND_APPLIANCE_FITTED){
      if(treatmentType !== PROPOSED){
        var er = "Treatment type '" + PROPOSED + "' is required when assessment is '" + ASSESS_AND_APPLIANCE_FITTED + "'";
        return {
          orthodontic_assessment: {
            assessment: er
          }
        }
      }
    }
  }
});