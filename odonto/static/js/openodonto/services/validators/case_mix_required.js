angular.module('opal.services').factory('CaseMixRequired', function(){

  // validators return a function that takes a patient
  // returns an object of
  // {stepApiName: field/step_error: errorMessage}

  // First line of address (house number and road name) is a mandatory item
  var FIELDS = {
    ability_to_communicate: "Ability to communicate",
    ability_to_cooperate: "Ability to co-operate",
    medical_status: "Medical status",
    oral_risk_factors: "Oral risk factors",
    access_to_oral_care: "Access to oral care",
    legal_and_ethical_barriers_to_care: "Legal and ethical barriers to care",
  }
  return function(editing){
    var errorObj = {};
    _.each(FIELDS, function(v, k){
      if(!editing.case_mix[k]){
        var errMsg = v + " is required";
        return errorObj[k] = errMsg;
      }
    });

    if(_.keys(errorObj).length){
      return {case_mix: errorObj};
    }
  }
});
