angular.module('opal.services').factory('Fp17OProposedTreatment', function(){
  /*
  * from an email in feb 2020,
  * Proposed Treatment mandatory on Assess/Appliance Fitted claims
  */
  return function(editing){
    "use strict";
    var assessmentReason = editing.orthodontic_assessment.assessment;
    var dataset = editing.orthodontic_data_set;
    var ASSESS_AND_APPLIANCE_FITTED = "Assess & appliance fitted"

    if(assessmentReason === ASSESS_AND_APPLIANCE_FITTED){
      if(!dataset.proposed){
        var er = "Proposed treatment is required when assessment is '" + ASSESS_AND_APPLIANCE_FITTED + "'";
        return {
          orthodontic_assessment: {
            assessment: er
          }
        }
      }
    }
  }
});