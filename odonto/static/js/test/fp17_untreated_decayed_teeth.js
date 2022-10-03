describe('Fp17UntreatedDecayedTeeth', function() {
  "use strict";
  var Fp17UntreatedDecayedTeeth;
  var editing;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17UntreatedDecayedTeeth  = $injector.get('Fp17UntreatedDecayedTeeth');
      });
      editing = {
        demographics: {},
        fp17_clinical_data_set: {},
				fp17_treatment_category: {},
				fp17_incomplete_treatment: {}
      };
  });

	it('should error if a patient is over 18, band 1,2 or 3 and there is no untreated decayed teeth', function(){
		editing.demographics.date_of_birth = moment("2000-12-05", "YYYY-MM-DD");
		editing.fp17_incomplete_treatment.date_of_acceptance = moment("2020-12-05", "YYYY-MM-DD");
		editing.fp17_treatment_category.treatment_category = "Band 1";
		var expected = {
			fp17_clinical_data_set: {
				untreated_decayed_teeth: "Adult bands 1, 2 and 3 require an entry of untreated decayed teeth"
			}
		}
		expect(Fp17UntreatedDecayedTeeth(editing)).toEqual(expected);
	});

	it('should not error if the recall interval is populated', function(){
		editing.demographics.date_of_birth = moment("2000-12-05", "YYYY-MM-DD");
		editing.fp17_incomplete_treatment.date_of_acceptance = moment("2020-12-05", "YYYY-MM-DD");
		editing.fp17_treatment_category.treatment_category = "Band 1";
		editing.fp17_clinical_data_set.untreated_decayed_teeth = 2;
		expect(Fp17UntreatedDecayedTeeth(editing)).toBe(undefined);
	});

	it('should not error if the recall interval is 0', function(){
		// note the form does not allow the recall interval to be 0
		// however should this be changed, lets make sure the validation
		// still works.
		editing.demographics.date_of_birth = moment("2000-12-05", "YYYY-MM-DD");
		editing.fp17_incomplete_treatment.date_of_acceptance = moment("2020-12-05", "YYYY-MM-DD");
		editing.fp17_treatment_category.treatment_category = "Band 1";
		editing.fp17_clinical_data_set.untreated_decayed_teeth = 0;
		expect(Fp17UntreatedDecayedTeeth(editing)).toBe(undefined);
	});

	it('should not error if the patient is not band 1, 2 or 3', function(){
		editing.demographics.date_of_birth = moment("2000-12-05", "YYYY-MM-DD");
		editing.fp17_incomplete_treatment.date_of_acceptance = moment("2020-12-05", "YYYY-MM-DD");
		editing.fp17_treatment_category.treatment_category = "Urgent treatment";
		expect(Fp17UntreatedDecayedTeeth(editing)).toBe(undefined);
	});

	it('should not error if the patient has no band', function(){
		editing.demographics.date_of_birth = moment("2000-12-05", "YYYY-MM-DD");
		editing.fp17_incomplete_treatment.date_of_acceptance = moment("2020-12-05", "YYYY-MM-DD");
		expect(Fp17UntreatedDecayedTeeth(editing)).toBe(undefined);
	});

	it('should not error date of birth is under 18', function(){
		editing.demographics.date_of_birth = moment("2003-12-05", "YYYY-MM-DD");
		editing.fp17_incomplete_treatment.date_of_acceptance = moment("2020-12-05", "YYYY-MM-DD");
		editing.fp17_treatment_category.treatment_category = "Band 1";
		expect(Fp17UntreatedDecayedTeeth(editing)).toBe(undefined);
	});

	it('should not error if there is no date of birth', function(){
		editing.fp17_incomplete_treatment.date_of_acceptance = moment("2020-12-05", "YYYY-MM-DD");
		editing.fp17_treatment_category.treatment_category = "Band 1";
		expect(Fp17UntreatedDecayedTeeth(editing)).toBe(undefined);
	});
});
