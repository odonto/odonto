angular.module('opal.services').factory('CovidTriageCovidStatusRequired', function(){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}

  return function(editing){
    if(!editing.covid_triage.covid_status){
      return {
        covid_triage: {
          covid_status: "COVID-19 status is required"
        }
      }
    }
  }
});
