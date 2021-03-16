angular.module('opal.services').factory('CovidTriageDateOfContactRequired', function(){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}

  return function(editing){
    if(!editing.covid_triage.date_of_contact){
      return {
        covid_triage: {
          date_of_contact: "Date of contact is required"
        }
      }
    }
  }
});
