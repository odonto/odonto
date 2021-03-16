angular.module('opal.services').factory('CovidTriageTimeOfContactRequired', function(){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}

  return function(editing){
    if(!editing.covid_triage.time_of_contact){
      return {
        covid_triage: {
          time_of_contact: "Time of contact is required"
        }
      }
    }
  }
});
