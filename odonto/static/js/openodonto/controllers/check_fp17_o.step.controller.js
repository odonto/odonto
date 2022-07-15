angular.module('opal.controllers').controller(
  'CheckFP17OStep',
  function(
    scope,
    step,
    episode,
    $timeout,
    $rootScope,
    FormValidation,
    NHSNumberValidator,
    DateOfBirthRequired,
    AddressRequired,
    ApplianceGreaterThanAssessment,
    CaseMixRequired,
    ProviderLocationNumberRequired,
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
    Fp17ORegulation11,
    Fp17OPhoneNumberRequired,
    Fp17OEmailRequired,
    Fp17OCommissionerApproval
){
  "use strict";
  $rootScope.isFormValid = null;
  $rootScope.showSummary = null;
  var validators = [
    DateOfBirthRequired,
    NHSNumberValidator,
    AddressRequired,
    CaseMixRequired,
    ApplianceGreaterThanAssessment,
    ProviderLocationNumberRequired,
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
    Fp17ORegulation11,
    // Fp17OPhoneNumberRequired, # enable when ALWAYS_DECLINE_EMAIL_PHONE
    // Fp17OEmailRequired, # is turned off.
    Fp17OCommissionerApproval
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
