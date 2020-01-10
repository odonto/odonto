angular.module('opal.services').factory('Fp17OAssessmentType', function(){
  /*
  * If there is a date of referral there must be one an assessment type
  */
  return function(editing){
    "use strict";
    var assessment = editing.orthodontic_assessment;

    if(assessment.date_of_referral && !assessment.assessment.length){
      return {
        "orthodontic_assessment": {
          "assessment": "An assessment type is required when there is a date of referral"
        }
      }
    }
  }
});
