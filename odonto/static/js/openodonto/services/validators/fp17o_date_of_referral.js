angular.module('opal.services').factory('Fp17ODateOfReferral', function(toMomentFilter){
  /*
  * Mandatory for all assessments where Date of Assessment is 01/04/19 or later.
  * Must be on or before the Date of Assessment
  * Cannot be a future date
  */
  return function(editing){
    "use strict";
    var assessment = editing.orthodontic_assessment;
    var dateOfReferral = toMomentFilter(assessment.date_of_referral);
    var dateOfAssessment = toMomentFilter(assessment.date_of_assessment);

    // if the date of assessment is after 1 April 2019, date of referral is required.
    var requiredAfterDate = moment('2019-04-01');

    if(dateOfAssessment){
      if(dateOfAssessment >= requiredAfterDate){
        if(!dateOfReferral){
          return {
            "orthodontic_assessment": {
              "date_of_referral": "Date of referral is required when there's a date of assessment"
            }
          }
        }
      }

      if(dateOfAssessment < dateOfReferral){
        return {
          "orthodontic_assessment": {
            "date_of_referral": "Date of referral must be equal or less than the date of assessment"
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
