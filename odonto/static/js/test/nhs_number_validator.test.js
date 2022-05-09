describe('NHSNumberValidator', function() {
  "use strict";
	var NHSNumberValidator;
	var editing;
	var getErr = function(somemsg){
		return {
			demographics: {
				nhs_number: somemsg
			}
		}
	}

	beforeEach(module('opal.services'));

  beforeEach(function(){
		inject(function($injector){
			NHSNumberValidator  = $injector.get('NHSNumberValidator');
		});
		editing = {demographics: {}};
	});

	it('should error if null', function(){
		var expected = getErr("NHS number is required");
		expect(NHSNumberValidator(editing)).toEqual(expected);
	});

	it('should error if empty', function(){
		var expected = getErr("NHS number is required");
		editing.demographics.nhs_number = "";
		expect(NHSNumberValidator(editing)).toEqual(expected);
	});

	it('should error if less than 10', function(){
		var expected = getErr("NHS number is too short");
		editing.demographics.nhs_number = "123456789";
		expect(NHSNumberValidator(editing)).toEqual(expected);
	});

	it('should error if more than 10', function(){
		var expected = getErr("NHS number is too long");
		editing.demographics.nhs_number = "12345678901";
		expect(NHSNumberValidator(editing)).toEqual(expected);
	});

	it('should error if it is alphanumeric', function(){
		var expected = getErr("NHS number should be numbers only");
		editing.demographics.nhs_number = "123456789A";
		expect(NHSNumberValidator(editing)).toEqual(expected);
	});

	describe('isValidNHSNumber', function(){
		it('should be valid', function(){
			var validNums = [
				"687 234 3060",
				"975 155 7305",
				"045 543 6029",
				"711 049 3547",
				"603 725 5857",
				"942 150 4356"
			];
			_.each(validNums, function(validNum){
				editing.demographics.nhs_number = validNum;
				expect(NHSNumberValidator(editing)).toBeUndefined();
			});
		});

		it('should be invalid', function(){
			var invalidNums = [
				"687 234 3061",
				"975 155 7306",
				"045 543 6031",
				"711 049 3548",
				"603 725 5858",
				"942 150 4357"
			]
			var expected = getErr("NHS number is invalid");
			_.each(invalidNums, function(invalidNum){
				editing.demographics.nhs_number = invalidNum;
				expect(NHSNumberValidator(editing)).toEqual(expected);
			});
		});
	})

});
