describe('ProviderLocationNumberRequired', function() {
  "use strict";
  var ProviderLocationNumberRequired;
  var editing;

  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        ProviderLocationNumberRequired  = $injector.get('ProviderLocationNumberRequired');
      });
      editing = {fp17_dental_care_provider: {}};
  });

  it('should error if its not set', function(){
    var expectedError = {
      fp17_dental_care_provider: {
        provider_location_number: "Provider location is required"
      }
    }
    expect(ProviderLocationNumberRequired(editing)).toEqual(expectedError);
  });

  it('should not error if it is set', function(){
    editing.fp17_dental_care_provider.provider_location_number = "Albion";
    expect(ProviderLocationNumberRequired(editing)).toBeUndefined();
  });
});