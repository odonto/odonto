angular.module('opal.services').factory('Fp17OAssessmentType', function(toMomentFilter, ValidatorUtils){
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
  * There is an unwritten rule that a patient cannot have a
  * a completion treatment type and an assessment.
  */
  var ASSESSMENT_AND_DEBOND = "Assessment and Debond – Overseas Patient";

  var validateAssessmentAndDebound = function(editing, step){
    /*
    * As defined by CCN52 this can only be used
    * •	date of assessment is 1 October 2022 or later
    * •	IOTN score is present or IOTN not applicable is selected
    * •	patient is from overseas
    * •	patient has an orthodontic appliance
    * •	patient has no history of NHS orthodontic treatment
    * •	patient does not pay for NHS dental treatment
    *
    * For our purposes this means
    * •	There must be an exemption
    * •	They cannot have a previous orthodontic claim
    *  (the IOTN validation is handled by the usual IOTN validation)
    */
    var err = null;
    var assessmentDate = toMomentFilter(editing.orthodontic_assessment.date_of_assessment);
    oct_first = moment('2022-10-01', 'YYYY-MM-DD');
    if(assessmentDate && assessmentDate.isBefore(oct_first, "d")){
      err = ASSESSMENT_AND_DEBOND + " cannot be used before 1/10/2022";
    }

    if(!ValidatorUtils.hasExemption(editing)){
      err = ASSESSMENT_AND_DEBOND + " requires at least one exemption";
    }

    priorAssessments = _.filter(step.other_assessments, function(otherAssessment){
      var otherAssessmentDate = toMomentFilter(otherAssessment.date);
      if(otherAssessmentDate && otherAssessmentDate.isBefore(assessmentDate)){
        return true;
      }
    });

    if(priorAssessments.length){
      err = ASSESSMENT_AND_DEBOND + " cannot be used if the patient has a previous orthodontic claim";
    }

    if(err){
      return {
        orthodontic_assessment: {
          assessment: err
        }
      }
    }
  }


  return function(editing, step){
    "use strict";
    var assessment = editing.orthodontic_assessment;
    var treatment = editing.orthodontic_treatment;
    var ASSESS_AND_APPLIANCE_FITTED = "Assess & appliance fitted";

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

    if(assessment.assessment){
      if(assessment.assessment === ASSESSMENT_AND_DEBOND){
        var err = validateAssessmentAndDebound(editing, step)
        if(err){
          return err
        }
      }
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
