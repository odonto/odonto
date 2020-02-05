angular.module('opal.services').factory('dateConflictCheck', function(toMomentFilter){
  "use strict";

  var checkBetween = function(ourRange, arrayOfRanges){
    var between = false;
    _.each(ourRange, function(dt){
      _.each(arrayOfRanges, function(range){
        if(range.length > 1){
          if(range[0] <= dt){
            if(dt <= range[1]){
              between = true
            }
          }
        }
      });
    });
    return between;
  }

  var checkSurrounds = function(ourRange, arrayOfRanges){
    var surrounds = false;
    if(ourRange.length < 2){
      return surrounds;
    }
    _.each(arrayOfRanges, function(theirRange){
      _.each(theirRange, function(dt){
        if(ourRange[0] <= dt){
          if(dt <= ourRange[1]){
            surrounds = true
          }
        }
      });
    })
    return surrounds;
  }

  var castRangeToMoments = function(range){
    return _.map(_.compact(range), toMomentFilter);
  }

  /*
  * Takes in an episodes array of dates and an array
  * of arrays of all other episodes.
  *
  * Arrays of dates can have one or more dates in them.
  *
  * Return true if our array of dates wrap any single date
  * in the dates of all other episodes.
  *
  * Return true if any of our array of dates is between
  * any of the date ranges
  *
  * so if passed [today] and [[yesterday, tomorrow]] it should return true
  * if passed [today] and [[today, tomorrow]] it should return true
  * if passed [yesterday, tomorrow] and [[today]] it should return true
  * if passed [two days ago, two days in the future], [[yesterday, today]] it should return true
  * if passed [yesterday, today] and [[two days ago, two days in the future]] it should return true
  *
  * if passed [yesterday, today] and [[three days ago, two days ago], [tomorrow, the day after tomorrow]]
  * it should return false
  */
  return function(ourRange, arrayOfRanges){
    var ourRange = castRangeToMoments(ourRange);
    arrayOfRanges = _.map(arrayOfRanges, function(range){
      return castRangeToMoments(range);
    });
    return checkBetween(ourRange, arrayOfRanges) || checkSurrounds(ourRange, arrayOfRanges);
  }
});