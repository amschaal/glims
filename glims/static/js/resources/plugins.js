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

angular.module('pluginModels', ['ngResource'])
.factory('ModelTypePlugin', ['$resource', function ($resource) {
  return $resource('/plugins/api/model_type_plugins/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    patch : { method : 'PATCH' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' },
  });
}]);

