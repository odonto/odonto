angular.module('opal.services').factory('DateOfBirthRequired', function(){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}


  // completion or last visit must be filled in and must be > date of acceptance
  return function(editing){
    if(!editing.demographics.date_of_birth){
      return {
        demographics: {
          date_of_birth: "Date of birth is required"
        }
      }
    }
  }
});
