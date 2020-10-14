angular.module("opal.controllers").controller("CaseMixHelper", function () {
  /*
  * A helper class to calculate the additional information around
  * case mixes
  */
  var CASE_MIX_FIELDS = {
    "ability_to_communicate": {
      "0": 0, "A": 2, "B": 4, "C": 8
    },
    "ability_to_cooperate": {
      "0": 0, "A": 3, "B": 6, "C": 12
    },
    "medical_status": {
      "0": 0, "A": 2, "B": 6, "C": 12
    },
    "oral_risk_factors": {
      "0": 0, "A": 3, "B": 6, "C": 12
    },
    "access_to_oral_care": {
      "0": 0, "A": 2, "B": 4, "C": 8
    },
    "legal_and_ethical_barriers_to_care": {
      "0": 0, "A": 2, "B": 4, "C": 8
    }
  }

  this.maxCode = function(caseMix){
    /*
    * Return highest case mix score
    */
    var val = 0;
    var code = "0";
    _.each(CASE_MIX_FIELDS, function(mapping, field){
      if(mapping[caseMix[field]] > val){
        val = mapping[caseMix[field]];
        code = caseMix[field];
      }
    });
    return code;
  }

  var getCaseMixScores = function(caseMix){
    var result = [];
    _.each(CASE_MIX_FIELDS, function(mapping, field){
      result.push(mapping[caseMix[field]]);
    });
    return result;
  }

  this.totalScore = function(caseMix){
    /*
    * Return the total score from all the case mix fields
    */
    return _.reduce(getCaseMixScores(caseMix), function(x, y){ return x + y}, 0);
  }

  this.band = function(caseMix){
    /*
    * return the band the total score falls in
    */
    var totalScore = this.totalScore(caseMix);
    if(totalScore === 0){
      return "Standard patient";
    }
    if(totalScore < 10){
      return "Some complexity";
    }
    if(totalScore < 20){
      return "Moderate complexity";
    }
    if(totalScore < 30){
      return "Severe complexity";
    }

    return "Extreme complexity";
  }
});
