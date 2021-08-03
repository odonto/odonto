angular.module('opal.services').factory('Fp17MaleMother', function(){
  return function(editing){
		if(editing.demographics.sex === 'Male'){
			if(editing.fp17_exemptions.expectant_mother){
				return {
					fp17_exemptions: {
						expectant_mother: "The patient is male"
					}
				}
			}
			if(editing.fp17_exemptions.nursing_mother){
				return {
					fp17_exemptions: {
						nursing_mother: "The patient is male"
					}
				}
			}
		}
  }
});
