angular.module('opal.services').factory('Fp17ODateOfApplianceFitted', function(dateConflictCheck){
  "use strict";

  return function(editing, step){
    var assessment = editing.orthodontic_assessment;
    if(assessment.date_of_appliance_fitted){
      if(dateConflictCheck([assessment.date_of_assessment, assessment.date_of_appliance_fitted], step.other_dates)){
        return {
          orthodontic_assessment: {
            date_of_appliance_fitted: "The FP17O overlaps with another FP17O of this patient"
          }
        }
      }
    }
  }
});