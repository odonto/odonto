angular.module('opal.services').factory('AddressRequired', function(){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}

  // First line of address (house number and road name) is a mandatory item
  return function(editing){
    if(!editing.demographics.house_number_or_name && !editing.demographics.street && !editing.demographics.protected){
      return {
        demographics: {
          street: "The patient address requires either a street name or a house number/name."
        }
      }
    }
  }
});
