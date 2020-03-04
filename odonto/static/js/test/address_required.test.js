describe('AddressRequired', function() {
  "use strict";
  var AddressRequired;
  var editing;

  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        AddressRequired  = $injector.get('AddressRequired');
      });
      editing = {demographics: {}};
  });

  it('should error if nothing is set', function(){
    var expected = {
      demographics: {
        street: "The patient address requires either a street name or a house number/name."
      }
    }
    expect(AddressRequired(editing)).toEqual(expected);
  });

  it('should not error if house number is set', function(){
    editing.demographics.house_number_or_name = "221b"
    expect(AddressRequired(editing)).toBe(undefined);
  });

  it('should not error if street is set', function(){
    editing.demographics.street = "Baker Street"
    expect(AddressRequired(editing)).toBe(undefined);
  });

  it('should not error if the address is protected', function(){
    editing.demographics.protected = true
    expect(AddressRequired(editing)).toBe(undefined);
  });
});