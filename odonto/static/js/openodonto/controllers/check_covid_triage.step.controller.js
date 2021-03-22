angular.module('opal.controllers').controller(
  'CheckCovidTriageStep', function(
    scope,
    step,
    episode,
    $timeout,
    $rootScope,
    FormValidation,
    CovidTriageCovidStatusRequired,
    CovidTriageDateOfContactRequired,
    CovidTriagePrimaryReasonRequired,
    CovidTriageTimeOfContact
){
  "use strict";
  $rootScope.isFormValid = null;
  $rootScope.showSummary = null;
  var validators = [
    CovidTriageCovidStatusRequired,
    CovidTriageDateOfContactRequired,
    CovidTriagePrimaryReasonRequired,
    CovidTriageTimeOfContact,
  ];

  var validate = function(){
    if(scope.form.$valid){
      var errors = FormValidation(scope.editing, validators, step);
      $rootScope.isFormValid = !_.size(errors);
      $rootScope.errors = errors;
    }
    else{
      $rootScope.isFormValid = false;
    }
  }
  scope.$watch("editing", validate, true);
  $rootScope.episodeSubmitted = step["episode_submitted"]

  $timeout(function(){
    scope.form.$setSubmitted();
    validate();
    $rootScope.showSummary = $rootScope.isFormValid || $rootScope.episodeSubmitted;
  });
});
