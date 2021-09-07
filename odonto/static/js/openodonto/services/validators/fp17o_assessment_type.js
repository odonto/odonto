angular.module('opal.services').factory('Fp17OAssessmentType', function(toMomentFilter){
  /*
  * If there is a date of referral there must be one an assessment type
  *
  * If there is no assessment or completion type compass rejects with
  * `No significant treatment on an EDI claim`
  *
  * If the previous type is assessment and appliance fitted,
  * they cannot have a subsequent claim that is an assessment.
  * ie they require a completion claim in between.
  *
  */
  return function(editing, step){
    "use strict";
    var assessment = editing.orthodontic_assessment;
    var treatment = editing.orthodontic_treatment;
    var treatmentType = editing.orthodontic_data_set.treatment_type;
    var PROPOSED = "Proposed"
    var ASSESS_AND_APPLIANCE_FITTED = "Assess & appliance fitted"

    if(assessment.date_of_referral && !assessment.assessment){
      return {
        "orthodontic_assessment": {
          "assessment": "An assessment type is required when there is a date of referral"
        }
      }
    }

    if(!assessment.assessment && !treatment.completion_type && !treatment.repair && !treatment.replacement){
      return {
        "orthodontic_assessment": {
          "assessment": "An assessment type, completion type, repair or reg 11 are required"
        },
        "orthodontic_treatment": {
          "completion_type": "An assessment type, completion type, repair or reg 11 are required",
          "repair": "An assessment type, completion type, repair or reg 11 are required",
          "replacement": "An assessment type, completion type, repair or reg 11 are required"
        }
      }
    }

    /*
    * Proposed treatment "Must be accompanied by Assess/Appliance Fitted"
    */
    if(assessment.assessment !== ASSESS_AND_APPLIANCE_FITTED && treatmentType === PROPOSED){
      var er = "Treatment type '" + PROPOSED + "' requires an assessment of '" + ASSESS_AND_APPLIANCE_FITTED + "'";
      return {
        orthodontic_assessment: {
          assessment: er
        }
      }
    }

    if(assessment.assessment){
      var otherAssessments = step.other_assessments
      var assessmentDate = toMomentFilter(editing.orthodontic_assessment.date_of_assessment);
      if(!assessmentDate){
        return;
      }
      _.each(otherAssessments, function(oa){
        oa.date = toMomentFilter(oa.date);
      });
      var previous = null;
      // get me the most recent fp17o before this one
      _.each(otherAssessments, function(oa){
        if(!oa.date){
          return;
        }
        var oaDate = oa.date.toDate();
        if(oaDate > assessmentDate.toDate()){
          return
        }
        if(!previous){
          previous = oa;
          return
        }
        if(previous.date && previous.date.toDate() < oaDate){
          previous = oa
        }
      });
      if(previous && previous.assessment && previous.assessment === ASSESS_AND_APPLIANCE_FITTED){
        return {
          orthodontic_assessment: {
            assessment: "This cannot have an assessment type as the patient's previous FP17O was 'Assess & appliance fitted'"
          }
        }
      }
    }
  }
});
