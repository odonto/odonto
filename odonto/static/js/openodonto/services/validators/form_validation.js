angular.module('opal.services').factory('FormValidation', function(){
  "use strict"

  var getValidationErrors = function(editing, validators, step){
    // errors are aggregated from the
    // validators and are of the form
    // {step_api_name: field_name: ["some errors"]}
    // form_name can also be step_base
    // isValid aggregates these and returns them
    var errors = {}
    _.each(validators, function(validator){
      var result = validator(editing, step);
      if(_.size(result)){
        _.each(result, function(step_error_obj, step_name){
          _.each(step_error_obj, function(error, field_name){
            if(!errors[step_name]){
              errors[step_name] = {};
            }
            errors[step_name][field_name] = error;
          });
        });
      }
    });
    return errors;
  }

  return getValidationErrors;
});