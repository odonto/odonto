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
});
