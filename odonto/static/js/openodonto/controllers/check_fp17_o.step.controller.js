angular.module('opal.controllers').controller(
  'CheckFP17OStep',
  function(
    scope,
    step,
    episode,
    $timeout,
    $rootScope,
    FormValidation,
    DateOfBirthRequired,
    AddressRequired,
    ApplianceGreaterThanAssessment,
    Fp17oUnder18,
    Fp17ODateOfReferral,
    Fp17ODateOfAssessment,
    Fp17OAssessmentType,
    AssessmentIOTN,
    TreatmentIOTN,
    Fp17ODateOfCompletion,
    Fp17OAged18InFullTimeEducation,
    Fp17OCompletionType
){
  "use strict";
  $rootScope.isFormValid = null;
  $rootScope.showSummary = null;
  var validators = [
    DateOfBirthRequired,
    AddressRequired,
    ApplianceGreaterThanAssessment,
    Fp17oUnder18,
    Fp17ODateOfReferral,
    Fp17ODateOfAssessment,
    Fp17OAssessmentType,
    AssessmentIOTN,
    TreatmentIOTN,
    Fp17ODateOfCompletion,
    Fp17OAged18InFullTimeEducation,
    Fp17OCompletionType
  ];

  var validate = function(){
    if(scope.form.$valid){
      var errors = FormValidation(scope.editing, validators);
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
