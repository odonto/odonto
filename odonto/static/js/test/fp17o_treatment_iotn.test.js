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
        },
        orthodontic_treatment: {
          iotn: undefined,
          completion_type: undefined
        }
      };
  });

  describe('Assessment IOTN and Treatment IOTN', function(){
    it('should not error if assessment IOTN is not set and treatment IOTN is', function(){
      editing.orthodontic_treatment.iotn = "1";
      expect(TreatmentIOTN(editing)).toBe(undefined);
    });

    it('should not error if assessment IOTN set and treatment IOTN is not', function(){
      editing.orthodontic_assessment.iotn = "1";
      expect(TreatmentIOTN(editing)).toBe(undefined);
    });

    it('should not error if assessment IOTN is the same as treatment IOTN', function(){
      editing.orthodontic_treatment.iotn = "1";
      editing.orthodontic_assessment.iotn = "1";
      var expected = {
        orthodontic_treatment: {iotn: "There cannot be both assessment IOTN and completion IOTN"}
      }
      expect(TreatmentIOTN(editing)).toEqual(expected);
    });
  });

  describe('Other completion types require any IOTN value', function(){
    it('should not error if completion type is set but not completed and IOTN is 1-5', function(){
      editing.orthodontic_treatment.iotn = "1";
      editing.orthodontic_treatment.completion_type = "Treatment discontinued";
      expect(TreatmentIOTN(editing)).toBe(undefined);
    });

    it('should not error if completion type is set but not completed and IOTN is N/A', function(){
      editing.orthodontic_treatment.iotn = "N/A";
      editing.orthodontic_treatment.completion_type = "Treatment discontinued";
      expect(TreatmentIOTN(editing)).toBe(undefined);
    });

    it('should error if completion type is set but not completed and IOTN is not set', function(){
      editing.orthodontic_treatment.completion_type = "Treatment discontinued";
      var expected = {
        orthodontic_treatment: {iotn: "'Treatment discontinued' requires an IOTN"}
      }
      expect(TreatmentIOTN(editing)).toEqual(expected);
    });
  });

  describe('Treatment completed requires an IOTN of 1-5', function(){
    it('should not error if completion type is treatment completed and IOTN is 1', function(){
      editing.orthodontic_treatment.iotn = "1";
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      expect(TreatmentIOTN(editing)).toBe(undefined);
    });

    it('should error if completion type is treatment completed IOTN is not set', function(){
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      var expected = {
        orthodontic_treatment: {iotn: "'Treatment completed' requires an IOTN of 1-5"}
      }
      expect(TreatmentIOTN(editing)).toEqual(expected);
    });

    it('should error if completion type is treatment completed IOTN is N/A', function(){
      editing.orthodontic_treatment.iotn = "N/A";
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      var expected = {
        orthodontic_treatment: {iotn: "'Treatment completed' requires an IOTN of 1-5"}
      }
      expect(TreatmentIOTN(editing)).toEqual(expected);
    });
  });
});
