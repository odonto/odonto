angular.module('opal.controllers').controller('CovidTriageStepCtrl', function(scope, step, episode, $rootScope){
  "use strict";
  /*
  * This controller does 2 things.
  * 1. The form input for time returns a javascript date object,
  *    the server wants a string in the form HH:MM:SS, so onload we create a local variable as a date
  *    when this local variable is updated we change that back into a HH:MM:SS on the editing variable
  * 2. The form has a check box for if the user is referred to urgent dental care. This is client
  *    only as the covid triage compass spec only requries a reason. The conrollter checks the checkbox
  *    if there is a reason.
  */


  var setUp = function(){
    scope.local = {referred: false, time_of_contact: null};
    if(scope.editing.covid_triage.referrered_to_local_udc_reason){
      scope.local.referred = true;
    }
    if(scope.editing.covid_triage.time_of_contact){
      /*
      * The html type time returns a js date where it only
      * uses the hour/minute parts
      * (it will use the seconds/milliseconds but we don't)
      */
      var hoursAndMinute = scope.editing.covid_triage.time_of_contact.split(":")
      var timeDate = new Date();
      timeDate.setHours(hoursAndMinute[0], hoursAndMinute[1], 0, 0);
      scope.local.time_of_contact = timeDate;
    }

  }

  scope.timeChange = function(){
    var timeDate = scope.local.time_of_contact;
    if(timeDate){
      scope.editing.covid_triage.time_of_contact = "" + timeDate.getHours() + ":" + timeDate.getMinutes() + ":00";
    }
    else{
      scope.editing.covid_triage.time_of_contact = null;
    }

    // The validate function is only set in the submit pathway by the check step.
    // Usually validate is triggered by $watch but this
    // will not trigger as we're in an ngchange so trigger validate manually
    if(scope.pathway.hasOwnProperty("validate")){
      scope.pathway.validate();
    }
  }

  setUp();
});
