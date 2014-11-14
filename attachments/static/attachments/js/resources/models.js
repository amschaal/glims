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
.factory('Note', ['$resource', function ($resource) {
  return $resource('/attachments/api/notes/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' }
  });
}]);

