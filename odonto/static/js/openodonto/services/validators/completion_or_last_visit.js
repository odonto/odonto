angular.module('opal.services').factory('CompletionOrLastVisit', function(){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: [errorMessages]}


  // completion or last visit must be filled in and must be > date of acceptance
  return function(editing){
    if(!editing.fp17_incomplete_treatment.completion_or_last_visit){
      return {
        fp17_incomplete_treatment: {
          completion_or_last_visit: "Date of completion or last visit is required"
        }
      }
    }
    if(!editing.fp17_incomplete_treatment.date_of_acceptance){
      return {
        fp17_incomplete_treatment: {
          date_of_acceptance: "Date of acceptance is required"
        }
      }
    }
    if(editing.fp17_incomplete_treatment.completion_or_last_visit < editing.fp17_incomplete_treatment.date_of_acceptance){
      return {
        fp17_incomplete_treatment: {
          completion_or_last_visit: "Date of completion must be later than date of acceptance"
        }
      }
    }
  }
});
