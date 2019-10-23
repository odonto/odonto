angular.module('opal.services').factory('ApplianceGreaterThanAssessment', function(){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}

  // First line of address (house number and road name) is a mandatory item
  return function(editing){
    if(editing.orthodontic_assessment.date_of_assessment){
      if(editing.orthodontic_assessment.date_of_appliance_fitted){
        if(editing.orthodontic_assessment.date_of_assessment > editing.orthodontic_assessment.date_of_appliance_fitted){
          return {
            orthodontic_assessment: {
              date_of_appliance_fitted: "The date of assessment cannot be later than the date the appliance is fitted."
            }
          }
        }
      }
    }
  }
});
