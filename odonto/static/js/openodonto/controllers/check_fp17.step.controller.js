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
    Fp17TreatmentCategory,
    Fp17DateOfAcceptance,
    Fp17Aged18InFullTimeEducation
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
    Fp17Aged18InFullTimeEducation
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

  $timeout(function(){
    scope.form.$setSubmitted();
    validate();
    $rootScope.showSummary = $rootScope.isFormValid;
  });
});
