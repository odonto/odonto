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
        // time is stored as HH:MM:SS so translate it to a date for the equality,
        var hoursAndMinute = editing.covid_triage.time_of_contact.split(":");
        ourDate.setHours(hoursAndMinute[0], hoursAndMinute[1], 0, 0);
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
