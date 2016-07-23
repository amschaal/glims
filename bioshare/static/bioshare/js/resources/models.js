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
		get: { method: 'GET'},
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
angular.module('bioshareModels', ['ngResource'])
.factory('ProjectShare', ['$resource', function ($resource) {
	var baseUrl = '/bioshare/api/project_shares/:id/';
	return $resource(baseUrl, {id:'@id'}, angular.extend({},standard_methods,{
		list_files : { method : 'GET', url: baseUrl+'list_files/' },
		link_paths : { method : 'POST', url: baseUrl+'link_paths/' }
	}));
}]);
