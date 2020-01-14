describe('Fp17Aged18InFullTimeEducation', function() {
  "use strict";
  var Fp17Aged18InFullTimeEducation;
  var editing;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17Aged18InFullTimeEducation  = $injector.get('Fp17Aged18InFullTimeEducation');
      });
      editing = {
        demographics: {},
        fp17_exemptions: {},
        fp17_incomplete_treatment: {},
      };
  });

  it('should return an error message if the patient is 19', function(){
    editing.demographics.date_of_birth = new Date(2000, 1, 1);
    editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2019, 1, 2);
    editing.fp17_exemptions.aged_18_in_full_time_education = true;
    var expected = {
      fp17_exemptions: {
        aged_18_in_full_time_education: "The patient was not 18"
      }
    }
    expect(Fp17Aged18InFullTimeEducation(editing)).toEqual(expected);
  });

  it('should return an error message if the patient is 17', function(){
    editing.demographics.date_of_birth = new Date(2000, 1, 1);
    editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2017, 1, 2);
    editing.fp17_exemptions.aged_18_in_full_time_education = true;
    var expected = {
      fp17_exemptions: {
        aged_18_in_full_time_education: "The patient was not 18"
      }
    }
    expect(Fp17Aged18InFullTimeEducation(editing)).toEqual(expected);
  });

  it('should not error if the exemption is not clicked', function(){
    editing.demographics.date_of_birth = new Date(2000, 1, 1);
    editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2019, 1, 2);
    editing.fp17_exemptions.aged_18_in_full_time_education = false;
    expect(Fp17Aged18InFullTimeEducation(editing)).toBe(undefined);
  });

  it('should not error if the patient is 18', function(){
    editing.demographics.date_of_birth = new Date(2000, 1, 1);
    editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2018, 1, 1);
    editing.fp17_exemptions.aged_18_in_full_time_education = true;
    expect(Fp17Aged18InFullTimeEducation(editing)).toBe(undefined);
  });

  it('should prioritise the date of assessment', function(){
    editing.demographics.date_of_birth = new Date(2000, 1, 1);
    editing.fp17_incomplete_treatment.date_of_acceptance = new Date(2018, 1, 1);
    editing.fp17_incomplete_treatment.completion_or_last_visit = new Date(2033, 1, 1);
    editing.fp17_exemptions.aged_18_in_full_time_education = true;
    expect(Fp17Aged18InFullTimeEducation(editing)).toBe(undefined);
  });
});