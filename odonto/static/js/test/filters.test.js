describe('filters', function() {
  "use strict";
  var extractionDisplay;

  beforeEach(module('opal.filters'));

  beforeEach(function(){
      inject(function($injector){
        extractionDisplay  = $injector.get('extractionDisplayFilter');
      });
  });


  describe('extractionDisplay', function(){
    it('should render an array with the single true value', function(){
      expect(extractionDisplay({ur_1: true})).toEqual(["UR_1"]);
    });

    it('should render an empty array if the value is false', function(){
      expect(extractionDisplay({ur_1: false})).toEqual([]);
    });

    it('should render  an empty array if the value is truthy', function(){
      expect(extractionDisplay({ur_1: "something"})).toEqual([]);
    });

    it('should render an array of everything that is true', function(){
      var val = {ur_a: true, ur_b: true, ur_1: false}
      expect(extractionDisplay(val)).toEqual(["UR_A", "UR_B"]);
    });
  });
});
