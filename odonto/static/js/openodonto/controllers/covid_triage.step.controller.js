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
    scope.local = {referred: false};
    if(scope.editing.covid_triage.referrered_to_local_udc_reason){
      scope.local.referred = true;
    }
  }

  setUp();
});
