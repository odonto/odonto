angular.module('opal.controllers').controller('CovidTriageStepCtrl', function(scope, step, episode, $rootScope){
  "use strict";
  /*
  * This controller does 2 things.
  * 1. Defaults the datetime of contact to now if its now already set.
  * 2. The form has a check box for if the user is referred to urgent dental care. This is client
  *    only as the covid triage compass spec only requries a reason. The conrollter checks the checkbox
  *    if there is a reason.
  */


  var setUp = function(){
    scope.local = {referred: false};
    if(scope.editing.covid_triage.referrered_to_local_udc_reason){
      scope.local.referred = true;
    }
    if(!scope.editing.covid_triage.datetime_of_contact){
      scope.editing.covid_triage.datetime_of_contact = new Date();
    }
  }

  setUp();
});
