angular.module('opal.services').factory('Fp17ODateOfApplianceFitted', function(dateConflictCheck){
  "use strict";

  return function(editing, step){
    var assessment = editing.orthodontic_assessment;
    var dates = _.pluck(step.overlapping_dates, "dates");
    if(assessment.date_of_appliance_fitted){
      if(dateConflictCheck([assessment.date_of_assessment, assessment.date_of_appliance_fitted], dates)){
        return {
          orthodontic_assessment: {
            date_of_appliance_fitted: "The FP17O overlaps with another FP17O of this patient"
          }
        }
      }
    }
  }
});