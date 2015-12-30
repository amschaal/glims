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

angular.module('glimsModels', ['ngResource'])
.factory('User', ['$resource', function ($resource) {
  return $resource('/api/users/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true }
  });
}])
.factory('Sample', ['$resource', function ($resource) {
  return $resource('/api/samples/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'POST', url: '/samples/api_update/'},
    create : { method : 'POST', url: '/samples/api_create/' },
    remove : { method : 'DELETE' }
  });
}])
.factory('Workflow', ['$resource', function ($resource) {
  return $resource('/api/workflows/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' }
  });
}])
.factory('Pool', ['$resource', function ($resource) {
  return $resource('/api/pools/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' }
  });
}]);

