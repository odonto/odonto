angular.module('opal.services').factory('CovidTriageTimeOfContact', function(toMomentFilter){
  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}

  return function(editing, step){
    if(!editing.covid_triage.time_of_contact){
      return {
        covid_triage: {
          time_of_contact: "Time of contact is required"
        }
      }
    }
    else{
      if(editing.covid_triage.date_of_contact){
        var existingDates = _.map(step.other_triage, toMomentFilter);
        var ourDate = new Date(editing.covid_triage.date_of_contact);
        var timeOfContact = editing.covid_triage.time_of_contact;
        ourDate.setHours(timeOfContact.getHours());
        ourDate.setMinutes(timeOfContact.getMinutes());
        var ourMoment = moment(ourDate);
        var error = false;
        _.each(existingDates, function(existingDate){
          if(ourMoment.isSame(existingDate)){
            error = true;
          }
        });
        if(error){
          return {
            covid_triage: {
              time_of_contact: "Date/time of contact matches a previously submitted triage claim"
            }
          }
        }
      }
    }
  }
});
