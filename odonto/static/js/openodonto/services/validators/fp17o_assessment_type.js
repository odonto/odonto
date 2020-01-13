angular.module('opal.services').factory('Fp17OAssessmentType', function(){
  /*
  * If there is a date of referral there must be one an assessment type
  *
  * If there is no assessment or completion type compass rejects with
  * `No significant treatment on an EDI claim`
  */
  return function(editing){
    "use strict";
    var assessment = editing.orthodontic_assessment;
    var treatment = editing.orthodontic_treatment;

    if(assessment.date_of_referral && !assessment.assessment){
      return {
        "orthodontic_assessment": {
          "assessment": "An assessment type is required when there is a date of referral"
        }
      }
    }

    if(!assessment.assessment && !treatment.completion_type){
      return {
        "orthodontic_assessment": {
          "assessment": "An assessment type or completion type are required"
        },
        "orthodontic_treatment": {
          "completion_type": "An assessment type or completion type are required"
        },
      }
    }
  }
});
