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

    if(cleanedNumber.length !== 11 || isNaN(cleanedNumber) || cleanedNumber.indexOf("0") !== 0){
      return {
        demographics: {
          phone_number: "Mobile number is incorrect"
        }
      }
    }
  }
});