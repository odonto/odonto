angular.module('opal.controllers').controller(
  'DisplaySummaryStep', function(scope, step, episode, $timeout, $rootScope, ExemptionsAndRemissionsValidator
){
  "use strict";
  $rootScope.isFormValid = null;
  $rootScope.showSummary = null;
  var validators = [
    ExemptionsAndRemissionsValidator
  ];
  var getValidationErrors = function(editing){
    // errors are aggregated from the
    // validators and are of the form
    // {step_api_name: field_name: ["some errors"]}
    // form_name can also be step_base
    // isValid aggregates these and returns them
    var errors = {}
    _.each(validators, function(validator){
      var result = validator(editing);
      if(_.size(result)){
        _.each(result, function(step_error_obj, step_name){
          _.each(step_error_obj, function(errors_array, field_name){
            if(!errors[step_name]){
              errors[step_name] = {};
            }
            if(!errors[step_name][field_name]){
              errors[step_name][field_name] = [];
            }
            _.each(errors_array, function(err){
              errors[step_name][field_name].push(err);
            })
          });
        });
      }
    });
    return errors;
  }


  var validate = function(){
    if(scope.form.$valid){
      var errors = getValidationErrors(scope.editing);
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
