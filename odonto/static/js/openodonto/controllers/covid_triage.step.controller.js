angular.module('opal.controllers').controller('CovidTriageStepCtrl', function(scope, step, episode){
  "use strict";

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
