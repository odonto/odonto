describe('LookupPatientCrl', function () {
    "use strict";
    var scope, $controller, controller, $location, DemographicsSearch;

    beforeEach(function () {
        module('opal.controllers');
        inject(function ($injector) {
            var $rootScope = $injector.get('$rootScope');
            scope = $rootScope.$new();
            scope.editing = {};
            $controller = $injector.get('$controller');
            $location = $injector.get('$location');
            DemographicsSearch = $injector.get('DemographicsSearch');
        });

        scope.pathway = {
            save_url: "/some_url"
        };

        controller = $controller('LookupPatientCrl', {
            scope: scope,
            step: {
                search_end_point: "/api/search_patient"
            },
            episode: {},
            DemographicsSearch: DemographicsSearch,
            $location: $location
        });
    });

    describe("lookup_nhs_number", function(){
        it("should search Demographics", function(){
            spyOn(DemographicsSearch, "find");
            scope.editing.demographics.nhs_number = "111";
            scope.lookup_nhs_number();
            expect(DemographicsSearch.find).toHaveBeenCalled();
            var calls = DemographicsSearch.find.calls.argsFor(0);
            expect(calls[0]).toBe(
                "/api/search_patient"
            );

            expect(calls[1]).toBe("111");
        });
    });

    describe("initialise", function () {
        it("should search automatically if search is passed in as a get parameter", function () {
            spyOn($location, "search").and.returnValue({
                nhs_number: "111"
            });

            spyOn(scope, "lookup_nhs_number");

            controller.initialise(scope);
            expect(scope.editing.demographics.nhs_number).toBe("111")
            expect(scope.lookup_nhs_number).toHaveBeenCalledWith();
            expect(scope.hideFooter).toBe(true);
        });

        it("should not search automatically if given the wrong get param", function () {
            spyOn($location, "search").and.returnValue({
                nhs_number: "111"
            });
            spyOn(scope, "lookup_nhs_number");
            expect(scope.state).toBe("initial");
            expect(scope.editing.demographics.nhs_number).toBe(undefined);
            expect(scope.hideFooter).toBe(true);
        });

        it("should handle it if there is no get param", function () {
            spyOn($location, "search").and.returnValue({});
            spyOn(scope, "lookup_nhs_number");
            expect(scope.state).toBe("initial");
            expect(scope.editing.demographics.nhs_number).toBe(undefined);
            expect(scope.hideFooter).toBe(true);
        });
    })

    describe("new_patient", function () {
        it('should handle new patient', function () {
            scope.new_patient();
            expect(scope.hideFooter).toBe(false);
            expect(scope.state).toBe("editing_demographics");
        });
    });

    describe("new_for_patient", function () {
        it("push the display name of the tags that the episode currently has on the scope", function () {
            var patient = {
                episodes: [
                    {tagging: [{tag1: true}, {tag2: true}]},
                    {tagging: [{tag1: true}]},
                ],
                demographics: [{
                    first_name: "Gerald"
                }]
            }
            scope.metadata = {};
            scope.metadata.tags = {
                tag1: {
                    display_name: "tag 1"
                }
            };
            scope.new_for_patient(patient);

            expect(scope.allTags).toEqual(["tag1"])
            expect(scope.editing.demographics).toEqual({
                first_name: "Gerald"
            });
            expect(scope.state).toBe("has_demographics");
            expect(scope.hideFooter).toBe(false);
        });
    });

    describe("showNext", function () {
        it("return true depending on state if depending on the state", function () {
            scope.state = "has_demographics"
            expect(scope.showNext()).toBe(true);
            scope.state = "editing_demographics"
            expect(scope.showNext()).toBe(true);
        });

        it("return false depending on state if depending on the state", function () {
            scope.state = "other";
            expect(scope.showNext()).toBe(false);
        });
    });

    describe("preSave", function () {
        it("should change the save url before we save if we have demographics", function () {
            var editing = {
                demographics: {
                    patient_id: 1
                }
            }
            scope.preSave(editing);
            expect(scope.pathway.save_url).toEqual("/some_url/1");
        });

        it("should not change the save url if we don't have demographics", function(){
            var editing = {};
            scope.preSave(editing);
            expect(scope.pathway.save_url).toEqual("/some_url");
        });
    });
});