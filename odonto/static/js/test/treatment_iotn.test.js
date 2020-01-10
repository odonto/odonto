describe('TreatmentIOTN', function() {
  "use strict";
  var TreatmentIOTN;
  var editing;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        TreatmentIOTN  = $injector.get('TreatmentIOTN');
      });
      editing = {
        orthodontic_assessment: {
          iotn: undefined,
          iotn_not_applicable: undefined
        },
        orthodontic_treatment: {
          iotn: undefined,
          iotn_not_applicable: undefined
        }
      };
  });

  describe('Assessment IOTN and Treatment IOTN', function(){
    it('should not error assessment IOTN is not set and treatment IOTN is', function(){
      editing.orthodontic_treatment.iotn = 1;
      expect(TreatmentIOTN(editing)).toBe(undefined);
    });

    it('should not error treatment IOTN set and treatment IOTN is not', function(){
      editing.orthodontic_assessment.iotn = 1;
      expect(TreatmentIOTN(editing)).toBe(undefined);
    });

    it('should not error if assessment IOTN is the same as treatment IOTN', function(){
      editing.orthodontic_treatment.iotn = 1;
      editing.orthodontic_assessment.iotn = 1;
      var expected = {
        orthodontic_treatment: {iotn: "There cannot be both assessment IOTN and treatment IOTN"}
      }
      expect(TreatmentIOTN(editing)).toEqual(expected);
    });
  });

  describe('Assessment IOTN not applicable and Treatment IOTN', function(){
    it('should not error if only IOTN not applicable is set', function(){
      editing.orthodontic_treatment.iotn_not_applicable = true;
      expect(TreatmentIOTN(editing)).toBe(undefined);
    });

    it('should error if both IOTN and IOTN not applicable are set', function(){
      editing.orthodontic_treatment.iotn = 1;
      editing.orthodontic_assessment.iotn_not_applicable = true;
      var expected = {
        orthodontic_treatment: {iotn: "Assessment IOTN is not applicable but treatment IOTN is set"}
      }
      expect(TreatmentIOTN(editing)).toEqual(expected);
    });
  });

  describe('Treatment IOTN and treatment IOTN not applicable are mutually exclusive', function(){
    it('should not error if only IOTN is set', function(){
      editing.orthodontic_treatment.iotn = 1;
      expect(TreatmentIOTN(editing)).toBe(undefined);
    });

    it('should not error if only IOTN not applicable is set', function(){
      editing.orthodontic_treatment.iotn_not_applicable = true;
      expect(TreatmentIOTN(editing)).toBe(undefined);
    });

    it('should error if both IOTN and IOTN not applicable are set', function(){
      editing.orthodontic_treatment.iotn = 1;
      editing.orthodontic_treatment.iotn_not_applicable = true;
      var expected = {
        orthodontic_treatment: {iotn_not_applicable: "There cannot be both IOTN and IOTN not applicable"}
      }
      expect(TreatmentIOTN(editing)).toEqual(expected);
    });
  });

  describe('Treatment IOTN not applicable and assessment IOTN not applicable cannot both be set', function(){
    it('should error if both treatment IOTN not applicable and assessment not applicable are set', function(){
      editing.orthodontic_assessment.iotn_not_applicable = true;
      editing.orthodontic_treatment.iotn_not_applicable = true;
      var expected = {
        orthodontic_treatment: {iotn_not_applicable: "Treatment IOTN not applicable and assessment IOTN not applicable cannot both be set"}
      }
      expect(TreatmentIOTN(editing)).toEqual(expected);
    });
  });
});
