angular.module('opal.services').factory('Fp17ODateOfAssessment', function(toMomentFilter, dateConflictCheck){
  /*
  * From the documentation:
  * Cannot be a future date
  * Mandatory item if Assess and Review (9012), Assess and Refuse (9013) or
  * Assess/Appliance Fitted (9014) is present
  *
  * Inferred from upstream rejection errors
  * If another episode for the same patient overlaps
  * then error
  */

  return function(editing, step){
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

    if(dateOfAssessment){
      if(dateOfAssessment && dateOfAssessment > moment()){
        return {
          orthodontic_assessment: {
            date_of_assessment: "Date of assessment cannot be in the future"
          }
        }
      }

      /*
      * Other_dates are a range of other episode dates
      * this can be a single date or multiple dates.
      *
      * If there are multiple dates and the date of assessment is
      * between them, then return an error.
      */
      var dates = _.pluck(step.overlapping_dates, "dates")
      if(dateConflictCheck([dateOfAssessment], dates)){
        return {
          orthodontic_assessment: {
            date_of_assessment: "The FP17O overlaps with another FP17O of this patient"
          }
        }
      }
    }
  }
});