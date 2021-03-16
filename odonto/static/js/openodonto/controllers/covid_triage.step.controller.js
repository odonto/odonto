angular.module('opal.controllers').controller('CovidTriageStepCtrl', function(scope, step, episode){
  "use strict";
  /*
  * This controller does 2 things.
  * 1. The form input for time returns a javascript date object,
  *    the server wants a string in the form HH:MM:SS, so we change it onload from string to date
  *    and back on save.
  * 2. The form has a check box for if the user is referred to urgent dental care. This is client
  *    only as the covid triage compass spec only requries a reason. The conrollter checks the checkbox
  *    if there is a reason.
  */


  var setUp = function(){
    scope.local = {referred: false};
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
      timeDate.setHours(hoursAndMinute[0]);
      timeDate.setMinutes(hoursAndMinute[1])
      scope.local.time_of_contact = timeDate;
    }
  }

  scope.preSave = function(editing){
    if(scope.local.time_of_contact){
      var timeDate = scope.local.time_of_contact;
      editing.covid_triage.time_of_contact = "" + timeDate.getHours() + ":" + timeDate.getMinutes();
    }
    return editing;
  }
  setUp();
});
