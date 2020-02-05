angular.module('opal.services').factory('Fp17DateOfAcceptance', function(dateConflictCheck){
  "use strict";
  /*
  * Date of acceptance cannot be a future date
  *
  * It cannot be between the date of acceptance/completion
  * of another FP17, unless its urgent/denture repair/bridge repair
  * (That filtering done on the server)
  */
  var URGENT_TREATMENT = "Urgent treatment";
  var DENTURE_REPAIRS = "Denture repairs";
  var BRIDGE_REPAIRS = "Bridge repairs";

  return function(editing, step){
    var dateOfAcceptance = editing.fp17_incomplete_treatment.date_of_acceptance;
    var category = editing.fp17_treatment_category.treatment_category;

    // date of acceptance is required but this
    // is validated as a requird field.
    if(!dateOfAcceptance){
      return;
    }

    if(dateOfAcceptance > moment()){
      return {
        fp17_incomplete_treatment: {
          date_of_acceptance: "Date of acceptance cannot be in the future"
        }
      }
    }




    if(category == URGENT_TREATMENT){
      return
    }
    if(category == DENTURE_REPAIRS){
      return
    }
    if(category == BRIDGE_REPAIRS){
      return
    }

    if(dateConflictCheck([dateOfAcceptance], step.overlapping_dates)){
      return {
        fp17_incomplete_treatment: {
          date_of_acceptance: "The FP17 overlaps with another FP17 of this patient"
        }
      }
    }
  }
});
