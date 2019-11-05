filters.filter('extractionDisplay', function(){
  "use strict";

  return function(record) {
    /*
    * Returns an array  of fields
    */
    var extractedTeeth = []
    _.each(record, function(v, k){
      if(v === true){
        extractedTeeth.push(k.toUpperCase());
      }
    })

    return extractedTeeth;
  };
});
