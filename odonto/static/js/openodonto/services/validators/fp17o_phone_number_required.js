angular.module('opal.services').factory('Fp17OPhoneNumberRequired', function(toMomentFilter){
  /*
  * from an email in feb 2020, phone number or phone number declined
  * are mandatory when submitted in FP17O
  */
  return function(editing){
    "use strict";
    if(editing.demographics.patient_declined_phone){
      return;
    }

    var number = editing.demographics.phone_number;

    if(!number || !number.length){
      return {
        demographics: {
          phone_number: "Mobile number is required"
        }
      }
    }

    var cleanedNumber = number.split("-").join("")
    cleanedNumber = cleanedNumber.split(" ").join("");
    var errorStr = null;
    if(cleanedNumber.length > 11){
      errorStr = "Mobile number is too long";
    }
    else if(cleanedNumber.length < 11){
      errorStr = "Mobile number is too short";
    }
    else if(isNaN(cleanedNumber)){
      errorStr = "Mobile number is not a number";
    }
    else if(cleanedNumber.indexOf("0")){
      errorStr = "Mobile number must begin with '0'";
    }

    if(errorStr){
      return {
        demographics: {
          phone_number: errorStr
        }
      }
    }
  }
});