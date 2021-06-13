angular.module('opal.services').factory('CovidTriagePrimaryReasonRequired', function(){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}

  return function(editing){
    if(!editing.covid_triage.primary_reason){
      return {
        covid_triage: {
          primary_reason: "Primary reason for call is required"
        }
      }
    }
  }
});
