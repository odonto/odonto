angular.module('opal.services').factory('Fp17ODateOfAssessment', function(toMomentFilter){
  /*
  * From the documentation:
  * Cannot be a future date
  * Mandatory item if Assess and Review (9012), Assess and Refuse (9013) or
  * Assess/Appliance Fitted (9014) is present
  */

  return function(editing){
    "use strict";
    var assessment = editing.orthodontic_assessment;
    var assessmentReason = assessment.assessment;
    var dateOfAssessment = toMomentFilter(assessment.date_of_assessment);
    if(assessmentReason && assessmentReason.length){
      if(!dateOfAssessment){
        return {
          orthodontic_assessment: {
            date_of_assessment: "Date of assessment is required when there is an assessment type"
          }
        }
      }
    }

    if(dateOfAssessment && dateOfAssessment > moment()){
      return {
        orthodontic_assessment: {
          date_of_assessment: "Date of assessment cannot be in the future"
        }
      }
    }
  }
});