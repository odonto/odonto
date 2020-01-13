describe('Fp17ODateOfCompletion', function() {
  "use strict";
  var Fp17ODateOfCompletion;
  var editing;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));


  beforeEach(function(){
    inject(function($injector){
      Fp17ODateOfCompletion  = $injector.get('Fp17ODateOfCompletion');
    });
    editing = {
      orthodontic_treatment: {}
    };
  });

  describe('if there is a completion type, date of completion is required', function(){
    it('should error if there is a completion type and no date of completion', function(){
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      var result = Fp17ODateOfCompletion(editing);
      var error = result.orthodontic_treatment.date_of_completion;
      expect(error).toBe("Date of completion or last visit is required when there is a completion type");
    });

    it('should not error if there is an completion type and no date of completion', function(){
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      editing.orthodontic_treatment.date_of_completion = moment('2019-04-05').toDate();
      var result = Fp17ODateOfCompletion(editing);
      expect(result).toBeUndefined();
    });
  });

  describe('date of completion cannot be in the future', function(){
    it('should error if the date of completion type is not in the future', function(){
      editing.orthodontic_treatment.completion_type = "Treatment completed";
      editing.orthodontic_treatment.date_of_completion = moment().add(2, "d").toDate();
      var result = Fp17ODateOfCompletion(editing);
      var error = result.orthodontic_treatment.date_of_completion;
      expect(error).toBe("Date of completion or last visit cannot be in the future");
    });

    it('should not error if there is no date of completion', function(){
      var result = Fp17ODateOfCompletion(editing);
      expect(result).toBeUndefined();
    });
  });
});