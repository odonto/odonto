angular.module('opal.services').factory('Fp17ODateOfCompletion', function(toMomentFilter){
  /*
  * Date of completion is required if there is a completion type.
  * This is implied by the documentation from
  * "Mandatory item on form 2 of active treatment"
  *
  * Also it cannot be in the future.
  */

  return function(editing){
    "use strict";
    var completion_type = editing.orthodontic_treatment.completion_type;
    var dateOfCompletion = toMomentFilter(editing.orthodontic_treatment.date_of_completion);

    if(completion_type && completion_type.length){
      if(!dateOfCompletion){
        return {
          orthodontic_treatment: {
            date_of_completion: "Date of completion or last visit is required when there is a completion type"
          }
        }
      }
    }

    if(dateOfCompletion && dateOfCompletion > moment()){
      return {
        orthodontic_treatment: {
          date_of_completion: "Date of completion or last visit cannot be in the future"
        }
      }
    }
  }
});