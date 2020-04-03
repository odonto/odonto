describe('Fp17OPhoneNumberRequired', function() {
  "use strict";
  var Fp17OPhoneNumberRequired;
  var editing, requiredError, inCorrectError, expected;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17OPhoneNumberRequired  = $injector.get('Fp17OPhoneNumberRequired');
      });
      editing = {
        demographics: {},
      };

      requiredError = {
        demographics: {
          phone_number: "Mobile number is required"
        }
      }
      inCorrectError = {
        demographics: {
          phone_number: "Mobile number is incorrect"
        }
      }
  });

  var getError = function(errStr){
    return {demographics: {phone_number: errStr}};
  }

  it('should error if the field is empty', function(){
    expect(Fp17OPhoneNumberRequired(editing)).toEqual(requiredError);
  });

  it('should error if its a zero length string', function(){
    editing.demographics.phone_number = "";
    expect(Fp17OPhoneNumberRequired(editing)).toEqual(requiredError);
  });

  it('should error if the field contains letters', function(){
    editing.demographics.phone_number = "0785 832 197a";
    expected = getError("Mobile number is not a number");
    expect(Fp17OPhoneNumberRequired(editing)).toEqual(expected);
  });

  it('should error if the field is too long', function(){
    editing.demographics.phone_number = "0785 832 1971 12";
    expected = getError("Mobile number is too long");
    expect(Fp17OPhoneNumberRequired(editing)).toEqual(expected);
  });

  it('should error if the field is too short', function(){
    editing.demographics.phone_number = "0785 832 19";
    expected = getError("Mobile number is too short");
    expect(Fp17OPhoneNumberRequired(editing)).toEqual(expected);
  });

  it("should error if the number doesn't start with 0", function(){
    editing.demographics.phone_number = "1785 832 1990";
    expected = getError("Mobile number must begin with '0'");
    expect(Fp17OPhoneNumberRequired(editing)).toEqual(expected);
  });

  it('should not error if the patient has declined', function(){
    editing.demographics.patient_declined_phone = true;
    expect(Fp17OPhoneNumberRequired(editing)).toBe(undefined);
  });

  it('should not error if it is just a number', function(){
    editing.demographics.phone_number = "07858321971";
    expect(Fp17OPhoneNumberRequired(editing)).toBe(undefined);
  });

  it('should not error if it is a number with dashes in it', function(){
    editing.demographics.phone_number = "0785-832-1971";
    expect(Fp17OPhoneNumberRequired(editing)).toBe(undefined);
  });

  it('should not error if it is a number with spaces in it', function(){
    editing.demographics.phone_number = "0785 832 1971";
    expect(Fp17OPhoneNumberRequired(editing)).toBe(undefined);
  });
});