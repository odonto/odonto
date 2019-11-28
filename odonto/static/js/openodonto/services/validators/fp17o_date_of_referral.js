angular.module('opal.services').factory('Fp17ODateOfReferral', function(toMomentFilter){
  /*
  * From the documentation:
  * Mandatory for all assessments where Date of Assessment is 01/04/19 or later.
  * Must be on or before the Date of Assessment
  * Cannot be a future date
  */
  return function(editing){
    "use strict";
    var assessment = editing.orthodontic_assessment;
    var dateOfReferral = toMomentFilter(assessment.date_of_referral);
    var dateOfAssessment = toMomentFilter(assessment.date_of_assessment);

    if(dateOfAssessment){
      if(!dateOfReferral){
        return {
          "orthodontic_assessment": {
            "date_of_referral": "Date of referral is required when there's a date of assessment"
          }
        }
      }

      if(dateOfAssessment < dateOfReferral){
        return {
          "orthodontic_assessment": {
            "date_of_referral": "Date of referral must be the same day or before the date of assessment"
          }
        }
      }
    }

    if(dateOfReferral > moment()){
      return {
        "orthodontic_assessment": {
          "date_of_referral": "Date of referral cannot be in the future"
        }
      }
    }
  }
});
