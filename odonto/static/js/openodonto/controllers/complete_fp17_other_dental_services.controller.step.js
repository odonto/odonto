angular.module('opal.controllers').controller('FP17IncompleteTreatmentCtrl', function(scope, step, episode, $timeout){

  scope.treatmentOnReferralError = false;
  scope.freeRepairOrReplacement = false;
  scope.furtherTreatmentWithin2Months = false;

  var validateTreatmentOnReferralError = function(){
    var category = scope.editing.fp17_treatment_category.treatment_category;
    var treatment_on_referral = scope.editing.fp17_other_dental_services.treatment_on_referral;
    scope.treatmentOnReferralError = !category && treatment_on_referral
    return scope.treatmentOnReferralError;
  }

  var validatefurtherTreatmentWithin2Months = function(){
    var category = scope.editing.fp17_treatment_category.treatment_category;
    var further_treatment_within_2_months = scope.editing.fp17_other_dental_services.further_treatment_within_2_months;
    scope.furtherTreatmentWithin2Months = !category && further_treatment_within_2_months
    return scope.furtherTreatmentWithin2Months;
  }

  var validateFreeRepairOrReplacement = function(){
    var category = scope.editing.fp17_treatment_category.treatment_category;
    var urgent = scope.editing.fp17_treatment_category.urgent_treatment;
    var treatmentOnReferral = scope.editing.fp17_other_dental_services.free_repair_or_replacement;
    var invalidCategories = ["Band 2", "Band 3"];
    var validCategories = _.contains(invalidCategories, category) || urgent;
    scope.freeRepairOrReplacement = treatmentOnReferral && !validCategories;
    return scope.freeRepairOrReplacement;
  }

  var validate = function(){
    var isInvalid = false;
    isInvalid = validateTreatmentOnReferralError() || isInvalid;
    isInvalid = validatefurtherTreatmentWithin2Months() || isInvalid;
    isInvalid = validateFreeRepairOrReplacement() || isInvalid;
    scope.pathway.errors = isInvalid;
  }

  scope.$watch("editing.fp17_treatment_category.treatment_category", function(){
    validate();
  });

  scope.$watch("editing.fp17_treatment_category.urgent_treatment", function(){
    validate();
  });

  scope.$watch("editing.fp17_other_dental_services.treatment_on_referral", function(){
    validate();
  });

  scope.$watch("editing.fp17_other_dental_services.free_repair_or_replacement", function(){
    validate();
  });

  scope.$watch("editing.fp17_other_dental_services.further_treatment_within_2_months", function(){
    validate();
  });
});
