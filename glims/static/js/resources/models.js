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

var standard_methods = {
	    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
	    save : { method : 'PUT' },
	    patch : { method : 'PATCH' },
	    create : { method : 'POST' },
	    remove : { method : 'DELETE' }
	  };
//	function file_manager_methods(baseURL){
//		var file_manager_methods  = {
//				list_files : { method : 'PUT', url: baseURL+'' },
//			    download : { method : 'PATCH' },
//			}
//	}
angular.module('glimsModels', ['ngResource'])
.factory('ModelType', ['$resource', function ($resource) {
  return $resource('/api/model_types/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true }
  });
}])
.factory('Status', ['$resource', function ($resource) {
  return $resource('/api/statuses/:id/', {id:'@id'}, standard_methods);
}])
.factory('User', ['$resource', function ($resource) {
  return $resource('/api/users/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true }
  });
}])
.factory('Sample', ['$resource', function ($resource) {
  return $resource('/api/samples/:id/', {id:'@id'}, standard_methods);
}])
.factory('Project', ['$resource', function ($resource) {
  return $resource('/api/projects/:id/', {id:'@id'}, standard_methods);
}])
.factory('Pool', ['$resource', function ($resource) {
  return $resource('/api/pools/:id/', {id:'@id'}, standard_methods);
}]);
