angular.module('opal.services').factory('Fp17OEmailRequired', function(toMomentFilter){
  /*
  * from an email in feb 2020, phone number or phone number declined
  * are mandatory when submitted in FP17O
  */
  return function(editing){
    "use strict";
    if(editing.demographics.patient_declined_email){
      return;
    }

    var email = editing.demographics.email;

    if(!email || !email.length){
      return {
        demographics: {
          email: "Email is required"
        }
      }
    }

    function validateEmail(email) {
      // A simple readable sanity test to catch
      // obvious mistakes in an email
      var re = /^\S+@\S+\.\S+$/;
      return re.test(String(email).toLowerCase());
    }

    var cleanedNumber = email.split("-").join("")
    cleanedNumber = cleanedNumber.split(" ").join("");

    if(!validateEmail(email)){
      return {
        demographics: {
          email: "Email is incorrect"
        }
      }
    }
  }
});