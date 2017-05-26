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

angular.module('tracker-plugin',['ngResource'])
//.run(function($rootScope) {
//    $rootScope.attachments_object = {};
//})
.factory('Category', ['$resource', function ($resource) {
  return $resource('/tracker/api/categories/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' }
  });
}])
.factory('Log', ['$resource', function ($resource) {
  return $resource('/tracker/api/logs/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' },
    set_statuses : {url:'/tracker/api/logs/set_statuses/',method:'POST'}
  });
}])
.factory('Export', ['$resource', function ($resource) {
  return $resource('/tracker/api/exports/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' },
    remove_logs : {url:'/tracker/api/exports/:id/remove_logs/',method:'POST'},
    add_logs : {url:'/tracker/api/exports/:id/add_logs/',method:'POST'}
  });
}]);

