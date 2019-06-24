describe('DemographicsSearch', function () {
    "use strict";
    var DemographicsSearch, $window, $httpBackend, ngProgressLite;
    var episode = {
        id: 10,
        demographics: [{
            patient_id: 12
        }]
    };

    var apiEndPoint, hn, callBacks, response;

    beforeEach(function () {
        module('opal.controllers');
        module('opal.services');
        inject(function ($injector) {
            DemographicsSearch = $injector.get('DemographicsSearch');
            $window = $injector.get('$window');
            $httpBackend = $injector.get('$httpBackend');
            // ngProgressLite = $injector.get('ngProgressLite');
        });

        apiEndPoint = "/search/";
        hn = "111";
        callBacks = {
            patient_found_in_application: jasmine.createSpy(),
            patient_not_found: jasmine.createSpy()
        };

        response = {
            patient: {
                demographics: [{
                    first_name: "Jane",
                    surname: "Doe",
                    nhs_number: "111"
                }]
            }
        };

        spyOn($window, "alert");
    });

    afterEach(function () {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    });

    it("should throw an error if there is an unexpected call back passed in", function () {
        callBacks["unexpected"] = "fail"
        expect(function () { DemographicsSearch.find(apiEndPoint, hn, callBacks); }).toThrow();
    });

    it("should call patient found in application", function () {
        response.status = "patient_found_in_application";
        $httpBackend.expectGET('/search/?nhs_number=111').respond(response);
        DemographicsSearch.find(apiEndPoint, hn, callBacks);
        $httpBackend.flush();
        expect(callBacks.patient_found_in_application).toHaveBeenCalledWith(response.patient);
    });

    it("should call patient not found", function () {
        response = {status: "patient_not_found"};
        $httpBackend.expectGET('/search/?nhs_number=111').respond(response);
        DemographicsSearch.find(apiEndPoint, hn, callBacks);
        $httpBackend.flush();
        expect(callBacks.patient_not_found).toHaveBeenCalledWith();
    });

    it("should handle an unexpected response", function () {
        response = {status: "strange"};
        $httpBackend.expectGET('/search/?nhs_number=111').respond(response);
        DemographicsSearch.find(apiEndPoint, hn, callBacks);
        $httpBackend.flush();
        expect($window.alert).toHaveBeenCalledWith("DemographicsSearch could not be loaded");
    });

    it("should handle http error cases", function () {
        $httpBackend.expectGET('/search/?nhs_number=111').respond(
            404, {'error': 'page not found'}
        );

        DemographicsSearch.find(apiEndPoint, hn, callBacks);
        $httpBackend.flush();
        expect($window.alert).toHaveBeenCalledWith("DemographicsSearch could not be loaded")
    });
});
