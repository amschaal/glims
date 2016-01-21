var transformDjangoRestResponse = function(data, headers){
	try {
        var jsonObject = JSON.parse(data); // verify that json is valid
        return jsonObject.results;
    }
    catch (e) {
        console.log("did not receive a valid Json: " + e)
    }
    return {};
}

angular.module('glimsModels')
.factory('BioinfoProject', ['$resource', function ($resource) {
  return $resource('/bioinformatics/api/bioinfo_projects/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' },
    users: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true, url: '/bioinformatics/api/bioinfo_projects/users/' },
  });
}])
;

