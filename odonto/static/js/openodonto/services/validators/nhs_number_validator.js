angular.module('opal.services').factory('NHSNumberValidator', function(){
	"use strict";

	var isValidNHSNumber = function(nhsNumber){
		/*
   	* https://www.datadictionary.nhs.uk/attributes/nhs_number.html
    * step 1, for the first 9 numbers multiple by 11 - idx,
    * step 2, sum them together
    * step 3, mod the result by 11
    * step 4, if the modded result is 0, then it becomes 11
    * step 5, subtract the result from 11
    * step 6, return result === nhs_number[9]
		*/

		var firstNineValues = _.first(nhsNumber, 9);

		// yields [10, 9, ... 2]
		var modifiers = _.range(2, 11).reverse();

		// yields [[nhsNumber[0], modifier[0]], [nhsNumber[1], modifier[1]] ...m ]
		var zipped = _.zip(firstNineValues, modifiers);

		// ends step 1
		var combined = _.map(zipped, function(x){
			return parseInt(x[0]) * x[1];
		});

		// step 2
		var summed = _.reduce(combined, function(x, y){ return x+y });

		// step 3
		var modulo = summed % 11;

		// step 4
		if(modulo === 0){
			modulo = 11;
		}

		// step 5
		var result = 11 - modulo;
		return result === parseInt(nhsNumber[9]);
	}

	return function(editing){
		var nhsNumber = editing.demographics.nhs_number;
		if(nhsNumber){
			// remove all spacess
			nhsNumber = nhsNumber.split(" ").join("");
		}
		if(!nhsNumber || !nhsNumber.length){
			return {
				demographics: {nhs_number: "NHS number is required"}
			}
		}
		if(nhsNumber.length < 10){
			return {
				demographics: {nhs_number: "NHS number is too short"}
			}
		}
		if(nhsNumber.length > 10){
			return {
				demographics: {nhs_number: "NHS number is too long"}
			}
		}
		if(isNaN(nhsNumber)){
			return {
				demographics: {nhs_number: "NHS number should be numbers only"}
			}
		}

		if(!isValidNHSNumber(nhsNumber)){
			return {
				demographics: {nhs_number: "NHS number is invalid"}
			}
		}

	};
});
