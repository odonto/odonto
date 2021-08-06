describe('Fp17MaleMother', function() {
  "use strict";
  var Fp17MaleMother;
  var editing = {};

  beforeEach(module('opal.services'));
  beforeEach(function(){
		inject(function($injector){
			Fp17MaleMother  = $injector.get('Fp17MaleMother');
		});
		editing.demographics = {};
		editing.fp17_exemptions = {};
	})

	it('should not error if the person is female', function(){
		editing.demographics.sex = 'Female';
		editing.fp17_exemptions.expectant_mother = true;
		editing.fp17_exemptions.nursing_mother = true;
		expect(Fp17MaleMother(editing)).toBeUndefined();
	});

	it('should not error if the person is not an expectant mother or a nursing mother', function(){
		editing.demographics.sex = 'Male';
		editing.fp17_exemptions.expectant_mother = false;
		editing.fp17_exemptions.nursing_mother = false;
		expect(Fp17MaleMother(editing)).toBeUndefined()
	});

	it('should error if the person is male and is an expectant mother', function(){
		var expected = {
			fp17_exemptions: {
				expectant_mother: "The patient is male"
			}
		}
		editing.demographics.sex = 'Male';
		editing.fp17_exemptions.expectant_mother = true;
		editing.fp17_exemptions.nursing_mother = false;
		expect(Fp17MaleMother(editing)).toEqual(expected);
	});

	it('should error if the person is male and is a nursing mother', function(){
		var expected = {
			fp17_exemptions: {
				nursing_mother: "The patient is male"
			}
		}
		editing.demographics.sex = 'Male';
		editing.fp17_exemptions.expectant_mother = false;
		editing.fp17_exemptions.nursing_mother = true;
		expect(Fp17MaleMother(editing)).toEqual(expected);
	});
});
