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

angular.module('sequencing',['ngResource'])
.factory('Machine', ['$resource', function ($resource) {
  return $resource('/sequencing/api/machines/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
//    save : { method : 'PUT' },
//    create : { method : 'POST' },
//    remove : { method : 'DELETE' }
  });
}])
.factory('Run', ['$resource', function ($resource) {
  return $resource('/sequencing/api/runs/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' }
  });
}])
.factory('Lane', ['$resource', function ($resource) {
  return $resource('/sequencing/api/lanes/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' }
  });
}]);

