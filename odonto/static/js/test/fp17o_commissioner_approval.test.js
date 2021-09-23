describe('Fp17OCommissionerApproval', function() {
  "use strict";
  var Fp17OCommissionerApproval;
  var editing, step;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));


  beforeEach(function(){
    inject(function($injector){
      Fp17OCommissionerApproval  = $injector.get('Fp17OCommissionerApproval');
    });
    editing = {
      fp17_exemptions: {},
      demographics: {},
      orthodontic_assessment: {}
    };
  });

  describe('If a patient is over 18 commissioner approval is required', function(){
    it('should error if the patient is over 18 and not commissioner approved', function(){
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      editing.demographics.date_of_birth = "01/01/1990";
      editing.orthodontic_assessment.date_of_referral = "02/01/2008";
      expect(Fp17OCommissionerApproval(editing)).toEqual({
        fp17_exemptions: {commissioner_approval: "Commissioner approval is required for patients 18 and over"}
      });
    });

    it('should not error if the patient is over 18', function(){
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      editing.demographics.date_of_birth = "02/01/1990";
      editing.orthodontic_assessment.date_of_referral = "01/01/2008";
      expect(Fp17OCommissionerApproval(editing)).toBe(undefined);
    });

    it('should not error if there is no dob', function(){
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      editing.orthodontic_assessment.date_of_referral = "01/01/2008";
      expect(Fp17OCommissionerApproval(editing)).toBe(undefined);
    });

    it('should not error if there is no date of referral', function(){
      editing.orthodontic_assessment.assessment = "Assessment & Review";
      editing.demographics.date_of_birth = "02/01/1990";
      expect(Fp17OCommissionerApproval(editing)).toBe(undefined);
    });

    it('should not error if there is no orthodontic assessment', function(){
      editing.demographics.date_of_birth = "02/01/1990";
      editing.orthodontic_assessment.date_of_referral = "01/01/2008";
      expect(Fp17OCommissionerApproval(editing)).toBe(undefined);
    });
  });

  describe('If a patient is marked as under 18 they cannot also have commissioner approval', function(){
    it('should be an error if a patient is both under 18 and has commissioner approval', function(){
      editing.fp17_exemptions.commissioner_approval = true;
      editing.fp17_exemptions.patient_under_18 = true;
      var expected = {
        fp17_exemptions: {
          commissioner_approval: "Commissioner approval is not allowed for patients under 18"
        }
      }
      expect(Fp17OCommissionerApproval(editing)).toEqual(expected);
    });

    it('should not error if a patient is not under 18 and has commissioner approval', function(){
      editing.fp17_exemptions.commissioner_approval = true;
      editing.fp17_exemptions.patient_under_18 = false;
      expect(Fp17OCommissionerApproval(editing)).toBe(undefined);
    });

    it('should not error if a patient is under 18 and does not have commissioner approval', function(){
      editing.fp17_exemptions.commissioner_approval = false;
      editing.fp17_exemptions.patient_under_18 = true;
      expect(Fp17OCommissionerApproval(editing)).toBe(undefined);
    });
  });
});
