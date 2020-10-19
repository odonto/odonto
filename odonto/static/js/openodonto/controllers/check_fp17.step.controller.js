angular.module('opal.controllers').controller(
  'CheckFP17Step', function(
    scope,
    step,
    episode,
    $timeout,
    $rootScope,
    FormValidation,
    ExemptionsAndRemissionsValidator,
    CompletionOrLastVisit,
    DateOfBirthRequired,
    AddressRequired,
    Fp17Under18,
    Fp17FurtherTreatment,
    Fp17TreatmentCategory,
    Fp17DateOfAcceptance,
    Fp17Aged18InFullTimeEducation,
    PretreatmentCovidTriageAssessments
){
  "use strict";
  $rootScope.isFormValid = null;
  $rootScope.showSummary = null;
  var validators = [
    ExemptionsAndRemissionsValidator,
    CompletionOrLastVisit,
    AddressRequired,
    DateOfBirthRequired,
    Fp17Under18,
    Fp17TreatmentCategory,
    Fp17DateOfAcceptance,
    Fp17FurtherTreatment,
    Fp17Aged18InFullTimeEducation,
    PretreatmentCovidTriageAssessments
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
