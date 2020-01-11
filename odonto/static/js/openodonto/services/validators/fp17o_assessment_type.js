angular.module('opal.services').factory('Fp17OAssessmentType', function(){
  /*
  * If there is a date of referral there must be one an assessment type
  *
  * If there is no assessment or resolution compass rejects with
  * `No significant treatment on an EDI claim`
  */
  return function(editing){
    "use strict";
    var assessment = editing.orthodontic_assessment;
    var treatment = editing.orthodontic_treatment;

    if(assessment.date_of_referral && !assessment.assessment.length){
      return {
        "orthodontic_assessment": {
          "assessment": "An assessment type is required when there is a date of referral"
        }
      }
    }

    if(!assessment.assessment.length && !treatment.resolution.length){
      return {
        "orthodontic_assessment": {
          "assessment": "An assessment type or resolution are required"
        },
        "orthodontic_treatment": {
          "resolution": "An assessment type or resolution are required"
        },
      }
    }
  }
});
