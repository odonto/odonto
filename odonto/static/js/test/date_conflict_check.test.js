describe('dateConflictCheck', function() {
  "use strict";
  var dateConflictCheck;
  var day1 = moment().subtract(10, "days");
  var day2 = moment().subtract(9, "days");
  var day3 = moment().subtract(8, "days");
  var day4 = moment().subtract(7, "days");
  var day5 = moment().subtract(6, "days");
  var day6 = moment().subtract(5, "days");


  beforeEach(module('opal.filters'));
  beforeEach(module('opal.services'));

  beforeEach(function(){
      inject(function($injector){
        dateConflictCheck  = $injector.get('dateConflictCheck');
      });
  });

  it('should return true if a single date, between two other dates ', function(){
    var ourDates = [day4];
    var theirDates = [[day3, day5]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(true);
  });

  it('should return true if a single date, that is the same as another dates ', function(){
    var ourDates = [day4];
    var theirDates = [[day3, day4]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(true);
  });

  it('should return true if there are two dates where the first is within two other dates', function(){
    var ourDates = [day4, day6];
    var theirDates = [[day3, day5]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(true);
  });

  it('should return true if two there are dates where the last is within two other dates ', function(){
    var ourDates = [day1, day4];
    var theirDates = [[day3, day5]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(true);
  });

  it('should return true if there are two dates between two other dates', function(){
    var ourDates = [day3, day4];
    var theirDates = [[day2, day5]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(true);
  });

  it('should return true if there are two days where another date is between them', function(){
    var ourDates = [day3, day5];
    var theirDates = [[day4]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(true);
  });

  it('should return false if the date is not in the other dates range', function(){
    var ourDates = [day1];
    var theirDates = [[day2, day3]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(false);
  });

  it('should return false if the range is not in the other dates range', function(){
    var ourDates = [day1, day2];
    var theirDates = [[day3, day4]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(false);
  });

  it('should return false if there is a range and the other dates date is not in it', function(){
    var ourDates = [day1, day2];
    var theirDates = [[day3]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(false);
  });

  it('should return false if there are no dates ', function(){
    var ourDates = [];
    var theirDates = [];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(false);
  });

  it('should return false if there are no dates where there other dates ', function(){
    var ourDates = [];
    var theirDates = [[day3]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(false);
  });

  it('should return false if there are no dates where there other ranges ', function(){
    var ourDates = [];
    var theirDates = [[day3, day4]];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(false);
  });

  it('should return false if there is a date where there are not other dates ', function(){
    var ourDates = [day1];
    var theirDates = [];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(false)
  });

  it('should return false if there is a range where there are not other dates ', function(){
    var ourDates = [day1, day2];
    var theirDates = [];
    expect(dateConflictCheck(ourDates, theirDates)).toBe(false)
  });
});