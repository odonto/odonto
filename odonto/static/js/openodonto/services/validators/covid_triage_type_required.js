angular.module('opal.services').factory('CovidTriageTypeRequired', function(){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}

  return function(editing){
    if(!editing.covid_triage.triage_type){
      return {
        covid_triage: {
          triage_type: "The type of triage is required"
        }
      }
    }
  }
});
