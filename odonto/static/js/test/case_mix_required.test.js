describe('CaseMixRequired', function() {
  "use strict";
  var editing, CaseMixRequired;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));


  beforeEach(function(){
    inject(function($injector){
      CaseMixRequired  = $injector.get('CaseMixRequired');
    });
    editing = {
      case_mix: {},
    }
  });

  it('should return an error if a field is not set', function(){
    editing.case_mix.medical_status = "A";
    editing.case_mix.ability_to_cooperate = null;
    editing.case_mix.ability_to_communicate = "A";
    editing.case_mix.medical_status = "A";
    editing.case_mix.oral_risk_factors = "A";
    editing.case_mix.access_to_oral_care = "A";
    editing.case_mix.legal_and_ethical_barriers_to_care = "A";

    expect(CaseMixRequired(editing)).toEqual(
      {case_mix: {ability_to_cooperate: "Ability to co-operate is required"}}
    )
  });

  it('should return a multiple errors if multiple fields are not set', function(){
    editing.case_mix.medical_status = "A";
    editing.case_mix.ability_to_cooperate = "0";
    editing.case_mix.ability_to_communicate = "0";
    editing.case_mix.medical_status = "A";
    editing.case_mix.oral_risk_factors = null;
    editing.case_mix.access_to_oral_care = null;
    editing.case_mix.legal_and_ethical_barriers_to_care = "A";

    expect(CaseMixRequired(editing)).toEqual(
      {
        case_mix: {
          oral_risk_factors: "Oral risk factors is required",
          access_to_oral_care: "Access to oral care is required"
        }
      }
    )
  });

  it('should not return an error if the field is set', function(){
    editing.case_mix.medical_status = "A";
    editing.case_mix.ability_to_cooperate = "A";
    editing.case_mix.ability_to_communicate = "A";
    editing.case_mix.medical_status = "A";
    editing.case_mix.oral_risk_factors = "A";
    editing.case_mix.access_to_oral_care = "A";
    editing.case_mix.legal_and_ethical_barriers_to_care = "A";
    expect(CaseMixRequired(editing)).toBeUndefined();
  });
});