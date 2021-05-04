angular.module('opal.services').factory('CovidTriageDateTimeOfContact', function(toMomentFilter){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}

  return function(editing, step){
    if(!editing.covid_triage.datetime_of_contact){
      return {
        covid_triage: {
          datetime_of_contact: "Date/time of contact is required"
        }
      }
    }
    else{
      var existingDates = _.map(step.other_triage, toMomentFilter);
      var ourDate = toMomentFilter(editing.covid_triage.datetime_of_contact);
      var error = false;
      _.each(existingDates, function(existingDate){
        if(ourDate.isSame(existingDate)){
          error = true;
        }
      });
      if(error){
        return {
          covid_triage: {
            datetime_of_contact: "Date/time of contact matches a previously submitted triage claim"
          }
        }
      }
    }
  }
});
