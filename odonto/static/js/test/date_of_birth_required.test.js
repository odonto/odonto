describe('DateOfBirthRequired', function() {
  "use strict";
  var DateOfBirthRequired;
  var editing;

  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        DateOfBirthRequired  = $injector.get('DateOfBirthRequired');
      });
      editing = {demographics: {}};
  });


  describe('is should return undefined if dob is not defined', function(){
    it('should render an array with the single true value', function(){
      editing.demographics.date_of_birth = new Date();
      expect(DateOfBirthRequired(editing)).toBe(undefined);
    });

    it('should return an error message if dob is not defined', function(){
      var expected = {demographics: {date_of_birth: "Date of birth is required"}};
      expect(DateOfBirthRequired(editing)).toEqual(expected);
    });

  });
});