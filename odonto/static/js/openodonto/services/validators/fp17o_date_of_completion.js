angular.module('opal.services').factory('Fp17ODateOfCompletion', function(toMomentFilter){
  /*
  * Date of completion is required if there is a resolution.
  * This is implied by the documentation from
  * "Mandatory item on form 2 of active treatment"
  *
  * Also it cannot be in the future.
  */

  return function(editing){
    "use strict";
    var resolution = editing.orthodontic_treatment.resolution;
    var dateOfCompletion = toMomentFilter(editing.orthodontic_treatment.date_of_completion);

    if(resolution && resolution.length){
      if(!dateOfCompletion){
        return {
          orthodontic_treatment: {
            date_of_completion: "Date of completion or last visit is required when there is a resolution"
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