describe('ValidatorUtils', function() {
  "use strict";
	var ValidatorUtils, editing;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        ValidatorUtils  = $injector.get('ValidatorUtils');
      });
      editing = {demographics: {}};
  });

	describe('eighteen_or_over', function(){
		it('should return null if date of birth is now set', function(){
			var otherDate = moment();
			expect(_.isNull(ValidatorUtils.eighteen_or_over(editing, otherDate))).toBe(true);
		});

		it('should return null if the other date is not set', function(){
			var otherDate = null;
			editing.demographics.date_of_birth = moment();
			expect(_.isNull(ValidatorUtils.eighteen_or_over(editing, otherDate))).toBe(true);
		});

		it('should return true if the patient is 18', function(){
			var otherDate = moment('2020-12-01', 'YYYY-MM-DD');
			editing.demographics.date_of_birth = moment('2002-02-1', 'YYYY-MM-DD');
			expect(ValidatorUtils.eighteen_or_over(editing, otherDate)).toBe(true);
		});

		it('should return true if the patient is 18 today', function(){
			var otherDate = moment('2020-02-01', 'YYYY-MM-DD');
			editing.demographics.date_of_birth = moment('2002-02-1', 'YYYY-MM-DD');
			expect(ValidatorUtils.eighteen_or_over(editing, otherDate)).toBe(true);
		});

		it('should return true if the patient is over 18', function(){
			var otherDate = moment('2022-12-01', 'YYYY-MM-DD');
			editing.demographics.date_of_birth = moment('2002-02-1', 'YYYY-MM-DD');
			expect(ValidatorUtils.eighteen_or_over(editing, otherDate)).toBe(true);
		});

		it('should return false if the patient is under 18', function(){
			var otherDate = moment('2020-01-31', 'YYYY-MM-DD');
			editing.demographics.date_of_birth = moment('2002-02-1', 'YYYY-MM-DD');
			expect(ValidatorUtils.eighteen_or_over(editing, otherDate)).toBe(false);
		});
	});

	describe('hasExemption', function(){
		it('should return true if the patient has an exemption', function(){
			editing.fp17_exemptions = {patient_under_18: true};
			expect(ValidatorUtils.hasExemption(editing)).toBe(true);
		});

		it('should return false if the patient does not have an exemption', function(){
			editing.fp17_exemptions = {};
			expect(ValidatorUtils.hasExemption(editing)).toBe(false);
		});
	});
});
