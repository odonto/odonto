angular.module('opal.services').factory('Fp17OCommissionerApproval', function(toMomentFilter){
  /*
  * For adult patients where an assessment has taken place, only
  * for courses of treatment on or after 01/04/2019, must be present
  * if one of the three assessment codes 9012 (Assess and Review).
  * 9013 (Assess and Refuse) or 9014 (Assess/Appliance Fitted) present.
  */
  return function(editing){
    "use strict";
    var dob = toMomentFilter(editing.demographics.date_of_birth);
    var referralDate = toMomentFilter(editing.orthodontic_assessment.date_of_referral);
    var commissionerApproval = editing.fp17_exemptions.commissioner_approval;
    var assessment = editing.orthodontic_assessment.assessment;

    if(assessment && assessment.length && dob && referralDate){
      var ageAtReferral = referralDate.diff(dob, "years", false);
      if(ageAtReferral > 17 && !commissionerApproval){
        return {
          fp17_exemptions: {
            commissioner_approval: "Commissioner approval is required for patients 18 and over"
          }
        }
      }
    }
  }
});
