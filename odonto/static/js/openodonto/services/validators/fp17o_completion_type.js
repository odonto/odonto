angular.module('opal.services').factory('Fp17OCompletionType', function(){
  /*
  * We have an exception of the nature
  * "Conflicting assessment and/or completion items on an EDI FP17O claim"
  *
  * The circumstances that create this are not explicit in the documentation
  *
  * It seems most likely caused by an assessment type of Assessment &
  * Refuse treatment and then a completion type which seems intuitively
  * problematic.
  *
  * Also the form guidance states for Assessment & Refuse" states
  *
  * "Cross this box if an assessment has been performed but NHS orthodontic
  * treatment is deemed unnecessary or inappropriate."
  *
  * Which backs this up.
  */
  return function(editing, step){
    "use strict";
    var assessment = editing.orthodontic_assessment;
    var treatment = editing.orthodontic_treatment;
    var treatmentType = editing.orthodontic_data_set.treatment_type
    var ASSESS_AND_REFUSE_TREATMENT = "Assess & refuse treatment"
    var COMPLETED = "Completed/Abandoned/Discontinued Treatment"


    if(assessment.assessment === ASSESS_AND_REFUSE_TREATMENT){
      if(treatment.completion_type){
        return {
          "orthodontic_treatment": {
            "completion_type": 'There cannot be a completion type and an assessment type of "Assess & refuse treatment"'
          }
        }
      }
    }



    if(!treatment.completion_type){
      if(treatmentType === COMPLETED){
        return {
          "orthodontic_treatment": {
            "completion_type": "Completion type is required when treatment type is '" + COMPLETED + "'"
          }
        }
      }
      return;
    }
    var dateOfCompletion = treatment.date_of_completion;
    if(!dateOfCompletion){
      return;
    }



    var dateAndCompletionType = []
    _.each(step.overlapping_dates, function(od){
      var lastDate = _.last(od.dates);
      if(lastDate < dateOfCompletion){
        dateAndCompletionType.push({
          date: lastDate,
          completion_type: od.completion_type
        });
      }
    });

    if(!dateAndCompletionType.length){
      return
    }
    dateAndCompletionType = _.sortBy(dateAndCompletionType, function(x){ return x.date });
    var mostRecent = _.last(dateAndCompletionType);
    if(mostRecent.completion_type){
      return {
        "orthodontic_treatment": {
          "completion_type": 'The previous claim was also a completion'
        }
      }
    }
  }
});
