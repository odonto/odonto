describe('Fp17ODateOfReferral', function() {
  "use strict";
  var Fp17ODateOfReferral;
  var editing;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17ODateOfReferral  = $injector.get('Fp17ODateOfReferral');
      });
      editing = {
        orthodontic_assessment: {}
      };
  });

  describe('required date of referral', function(){
    it('should error if date of referral is not there and the date of assessment is populated', function(){
      editing.orthodontic_assessment.date_of_referral = undefined;
      editing.orthodontic_assessment.date_of_assessment = moment('2019-04-05').toDate();
      var result = Fp17ODateOfReferral(editing);
      var error = result.orthodontic_assessment.date_of_referral;
      expect(error).toBe("Date of referral is required when there's a date of assessment");
    });

    it('should not error if date of assessment is not present', function(){
      editing.orthodontic_assessment.date_of_referral = undefined;
      editing.orthodontic_assessment.date_of_assessment = undefined;
      var result = Fp17ODateOfReferral(editing);
      expect(result).toBeUndefined();
    });
  });

  describe('date of referral must be less than date of assessment', function(){
    it('should error if the date of assessment is less than the date of referral', function(){
      editing.orthodontic_assessment.date_of_referral = moment('2019-04-06').toDate();;
      editing.orthodontic_assessment.date_of_assessment = moment('2019-04-05').toDate();
      var result = Fp17ODateOfReferral(editing);
      var error = result.orthodontic_assessment.date_of_referral;
      expect(error).toBe("Date of referral must be the same day or before the date of assessment");
    });

    it('should not error if the date of assessment is the same as the date of referral', function(){
      editing.orthodontic_assessment.date_of_referral = moment('2019-04-05').toDate();;
      editing.orthodontic_assessment.date_of_assessment = moment('2019-04-05').toDate();
      var result = Fp17ODateOfReferral(editing);
      expect(result).toBeUndefined();
    });

    it('should  not error if the date of referral is greater than the date of assessment', function(){
      editing.orthodontic_assessment.date_of_referral = moment('2019-04-04').toDate();;
      editing.orthodontic_assessment.date_of_assessment = moment('2019-04-05').toDate();
      var result = Fp17ODateOfReferral(editing);
      expect(result).toBeUndefined();
    });
  });

  describe('referral cannot be in the future', function(){
    it('should error if date of referral is in the future', function(){
      editing.orthodontic_assessment.date_of_referral = moment('2300-04-04').toDate();;
      editing.orthodontic_assessment.date_of_assessment = moment('2300-04-05').toDate();
      var result = Fp17ODateOfReferral(editing);
      var error = result.orthodontic_assessment.date_of_referral;
      expect(error).toBe("Date of referral cannot be in the future");
    });
  })
});