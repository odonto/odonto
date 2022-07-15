angular.module('opal.services').factory('Fp17OCompletionType', function(toMomentFilter){
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
  *
  * Additionally
  * treatment type Completed / Abandoned / Discontinued Treatment
  * "Must be accompanied by Treatment Abandoned (9161 1), Treatment
  * Discontinued (9161 2) or Treatment Completed (9161 3)"
  */
  return function(editing, step){
    "use strict";
    var assessment = editing.orthodontic_assessment;
    var treatment = editing.orthodontic_treatment;
    var ASSESS_AND_REFUSE_TREATMENT = "Assess & refuse treatment"


    if(assessment.assessment === ASSESS_AND_REFUSE_TREATMENT){
      if(treatment.completion_type){
        return {
          "orthodontic_treatment": {
            "completion_type": 'There cannot be a completion type and an assessment type of "Assess & refuse treatment"'
          }
        }
      }
    }

    var dateOfCompletion = treatment.date_of_completion;
    if(!dateOfCompletion){
      return;
    }



    var dateAndCompletionType = []
    _.each(step.overlapping_dates, function(od){
      var lastDate = toMomentFilter(_.last(od.dates));
      dateAndCompletionType.push({
        date: lastDate,
        completion_type: od.completion_type
      });
    });

    if(!dateAndCompletionType.length){
      return
    }

    var previous = null;
    var next = null;
    var ourCompletionDate = toMomentFilter(treatment.date_of_completion);

    dateAndCompletionType = _.sortBy(dateAndCompletionType, function(x){ return x.date.toDate() });

    _.each(dateAndCompletionType, function(dc){
      if(dc.date.isSame(ourCompletionDate, "d") || dc.date.isBefore(ourCompletionDate, "d")){
        previous = dc;
      }
      if(!next && (ourCompletionDate.isSame(dc.date) || ourCompletionDate.isBefore(dc.date))){
        next = dc;
      }
    })

    if(previous && previous.completion_type){
      return {
        "orthodontic_treatment": {
          "completion_type": 'The previous claim was also a completion'
        }
      }
    }
    if(next && next.completion_type){
      return {
        "orthodontic_treatment": {
          "completion_type": 'The next claim for this patient is also a completion'
        }
      }
    }
  }
});
