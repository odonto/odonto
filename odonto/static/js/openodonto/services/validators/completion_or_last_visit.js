angular.module('opal.services').factory('CompletionOrLastVisit', function(dateConflictCheck){
  "use strict";
  /*
  * The Date of completion or last visit is required.
  *
  * Date of completion or last visit cannot be a future date.
  * It must be greater than the date of acceptance.
  *
  * The date of acceptance and completion and last visit
  * cannot wrap another episodes date of acceptance
  * (which is brought through on the step from the server)
  */
  var getErr = function(someStr){
    return {
      fp17_incomplete_treatment: {
        completion_or_last_visit: someStr
      }
    }
  }

  var URGENT_TREATMENT = "Urgent treatment";
  var DENTURE_REPAIRS = "Denture repairs";
  var BRIDGE_REPAIRS = "Bridge repairs";


  return function(editing, step){
    var completionOrLastVisit = editing.fp17_incomplete_treatment.completion_or_last_visit;
    var category = editing.fp17_treatment_category.treatment_category;
    var dateOfAcceptance = editing.fp17_incomplete_treatment.date_of_acceptance;

    if(!completionOrLastVisit){
      return getErr("Date of completion or last visit is required")
    }

    if(completionOrLastVisit > moment()){
      return getErr("Date of acceptance cannot be in the future")
    }

    if(completionOrLastVisit < dateOfAcceptance){
      return getErr("Completion or last visit must be greater than the day of acceptance")
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

    if(dateConflictCheck([dateOfAcceptance, completionOrLastVisit], step.overlapping_dates)){
      return {
        fp17_incomplete_treatment: {
          date_of_acceptance: "The FP17 overlaps with another FP17 of this patient"
        }
      }
    }
  }
});
