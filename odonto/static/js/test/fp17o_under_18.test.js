describe('Fp17oUnder18', function() {
  "use strict";
  var Fp17oUnder18;
  var editing;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17oUnder18  = $injector.get('Fp17oUnder18');
      });
      editing = {
        demographics: {},
        fp17_exemptions: {},
        orthodontic_assessment: {},
        orthodontic_treatment: {}
      };
  });


  describe('if a patient has the under 18 exemption it should error if their dob is older', function(){
    it('should return an error message if dob is to recent', function(){
      editing.demographics.date_of_birth = new Date(1980, 1, 1);
      editing.orthodontic_assessment.date_of_referral = new Date(2019, 1, 1);
      editing.fp17_exemptions.patient_under_18 = true;
      var expected = {
        fp17_exemptions: {
          patient_under_18: "This patient is not under 18"
        }
      }
      expect(Fp17oUnder18(editing)).toEqual(expected);
    });

    it('should not error if the exemption is not clicked and the patient is not under 18', function(){
      editing.demographics.date_of_birth = new Date(1980, 1, 1);
      editing.orthodontic_assessment.date_of_referral = new Date(2019, 1, 1);
      editing.fp17_exemptions.patient_under_18 = false;
      expect(Fp17oUnder18(editing)).toBe(undefined);
    });

    it('should error if the exemption is not clicked and the patient is under 18', function(){
      editing.demographics.date_of_birth = new Date(2000, 1, 1);
      editing.orthodontic_assessment.date_of_referral = new Date(2017, 1, 1);
      editing.fp17_exemptions.patient_under_18 = false;
      var expected = {
        fp17_exemptions: {
          patient_under_18: "This patient is under 18"
        }
      }
      expect(Fp17oUnder18(editing)).toEqual(expected);
    });

    it('should not error if the exemption is not clicked and the patient is under 18 if it is a completion claim', function(){
      editing.demographics.date_of_birth = new Date(20160, 1, 1);
      editing.orthodontic_assessment.date_of_referral = new Date(2019, 1, 1);
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      editing.fp17_exemptions.patient_under_18 = false;
      expect(Fp17oUnder18(editing)).toBe(undefined);
    });

    it('should not error if the date of birth is under 18 years ago', function(){
      editing.demographics.date_of_birth = new Date(2015, 1, 1);
      editing.orthodontic_assessment.date_of_referral = new Date(2019, 1, 1);
      editing.fp17_exemptions.patient_under_18 = true;
      expect(Fp17oUnder18(editing)).toBe(undefined);
    });

    it('should error if the patient is just 18', function(){
      editing.demographics.date_of_birth = new Date(2002, 10, 1);
      editing.orthodontic_assessment.date_of_referral =  new Date(2020, 10, 1);
      editing.fp17_exemptions.patient_under_18 = true;
      var expected = {
        fp17_exemptions: {
          patient_under_18: "This patient is not under 18"
        }
      }
      expect(Fp17oUnder18(editing)).toEqual(expected);
    })

    it('should not error if the patient is nearly 18', function(){
      editing.demographics.date_of_birth = new Date(2002, 10, 10);
      editing.orthodontic_assessment.date_of_referral = new Date(2020, 10, 9);
      editing.fp17_exemptions.patient_under_18 = true;
      expect(Fp17oUnder18(editing)).toBe(undefined);
    })

    it('should prioritise the date of referral', function(){
      editing.demographics.date_of_birth = new Date(2003, 1, 1);
      editing.orthodontic_assessment.date_of_referral = new Date(2018, 1, 1);
      editing.orthodontic_assessment.date_of_assessment = new Date(2033, 1, 1);
      editing.fp17_exemptions.patient_under_18 = true;
      expect(Fp17oUnder18(editing)).toBe(undefined);
    });
  });
});
