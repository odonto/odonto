describe('Fp17OPhoneNumberRequired', function() {
  "use strict";
  var Fp17OEmailRequired;
  var editing, requiredError, inCorrectError;

  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        Fp17OEmailRequired  = $injector.get('Fp17OEmailRequired');
      });
      editing = {
        demographics: {},
      };

      requiredError = {
        demographics: {
          email: "Email is required"
        }
      }
      inCorrectError = {
        demographics: {
          email: "Email is incorrect"
        }
      }
  });

  it('should error if the field is empty', function(){
    expect(Fp17OEmailRequired(editing)).toEqual(requiredError);
  });

  it('should error if its a zero length string', function(){
    editing.demographics.email = "";
    expect(Fp17OEmailRequired(editing)).toEqual(requiredError);
  });

  it('should error if there is no @', function(){
    editing.demographics.email = "janedoe";
    expect(Fp17OEmailRequired(editing)).toEqual(inCorrectError);
  });

  it('should error if there is no .', function(){
    editing.demographics.email = "jane@doe";
    expect(Fp17OEmailRequired(editing)).toEqual(inCorrectError);
  });

  it('should error @ is before the .', function(){
    editing.demographics.email = "asdf.asfd@asdf";
    expect(Fp17OEmailRequired(editing)).toEqual(inCorrectError);
  });

  it('should not error if it is a correct email address', function(){
    editing.demographics.email = "janedoe@nhs.net";
    expect(Fp17OEmailRequired(editing)).toBe(undefined);
  });

  it('should if it is a correct email address with .s at the beginning', function(){
    editing.demographics.email = "jane.doe@nhs.net";
    expect(Fp17OEmailRequired(editing)).toBe(undefined);
  });
});