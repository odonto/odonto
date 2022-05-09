angular.module('opal.controllers').controller(
  'CheckFP17Step', function(
    scope,
    step,
    episode,
    $timeout,
    $rootScope,
    CaseMixRequired,
    FormValidation,
    ExemptionsAndRemissionsValidator,
    CompletionOrLastVisit,
    DateOfBirthRequired,
    NHSNumberValidator,
    AddressRequired,
    ProviderLocationNumberRequired,
    Fp17Under18,
    Fp17MaleMother,
    Fp17FurtherTreatment,
    Fp17TreatmentCategory,
    Fp17DateOfAcceptance,
    Fp17Aged18InFullTimeEducation,
    Fp17FreeRepaireReplacement
){
  "use strict";
  $rootScope.isFormValid = null;
  $rootScope.showSummary = null;
  var validators = [
    CaseMixRequired,
    ExemptionsAndRemissionsValidator,
    CompletionOrLastVisit,
    NHSNumberValidator,
    AddressRequired,
    DateOfBirthRequired,
    ProviderLocationNumberRequired,
    Fp17Under18,
    Fp17MaleMother,
    Fp17TreatmentCategory,
    Fp17DateOfAcceptance,
    Fp17FurtherTreatment,
    Fp17Aged18InFullTimeEducation,
    Fp17FreeRepaireReplacement
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
    $rootScope.showSummary = $rootScope.isFormValid && $rootScope.episodeSubmitted;
  });
});
