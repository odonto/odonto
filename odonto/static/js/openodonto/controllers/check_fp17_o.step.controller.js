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
    Fp17ODateOfApplianceFitted,
    Fp17OAssessmentType,
    FP17OAssessmentIOTN,
    Fp17OAssessmentAestheticComponent,
    TreatmentIOTN,
    Fp17OTreatmentAestheticComponent,
    Fp17ODateOfCompletion,
    Fp17OAged18InFullTimeEducation,
    Fp17OCompletionType,
    Fp17OPhoneNumberRequired,
    Fp17OEmailRequired,
    Fp17OProposedTreatment
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
    Fp17ODateOfApplianceFitted,
    Fp17OAssessmentType,
    FP17OAssessmentIOTN,
    Fp17OAssessmentAestheticComponent,
    TreatmentIOTN,
    Fp17OTreatmentAestheticComponent,
    Fp17ODateOfCompletion,
    Fp17OAged18InFullTimeEducation,
    Fp17OCompletionType,
    Fp17OPhoneNumberRequired,
    Fp17OEmailRequired,
    Fp17OProposedTreatment
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
