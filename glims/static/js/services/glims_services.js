angular.module('glimsServices',['glims.formly','glims.ui'])
.factory('DRFNgTableParams', ['NgTableParams','$http','$location', function(NgTableParams,$http,$location) {
	return function(url,ngparams,resource) {
		var params = {
//				page: 1, // show first page
//				filter:{foo:'bar'}, //filter stuff
				count: 10 // count per page
		}
		angular.merge(params,ngparams);
		return new NgTableParams(params, {
			filterDelay: 0,
			getData: function(params) {
				var url_params = params.url();
				var query_params = {page:url_params.page,page_size:url_params.count,ordering:params.orderBy().join(',').replace('+','')};
				angular.extend(query_params, params.filter());
				// ajax request to api
				return $http.get(url,{params:query_params}).then(function(response){
					params.total(response.data.count);
//					console.log('old state', $location.search())
//					angular.forEach(query_params,function(value,key){$location.search(key, value);});
//					console.log('query_params',query_params); 
					if (resource)
						return response.data.results.map(function(obj){return new resource(obj);});
					else
						return response.data.results;
				});
			}
		});
	};
}])
.factory('LocationSearchState', function($location) {
	//flatten/unflatten come from here: https://stackoverflow.com/questions/19098797/fastest-way-to-flatten-un-flatten-nested-json-objects
	function flatten(data) {
	    var result = {};
	    function recurse (cur, prop) {
	        if (Object(cur) !== cur) {
	            result[prop] = cur;
	        } else if (Array.isArray(cur)) {
	             for(var i=0, l=cur.length; i<l; i++)
	                 recurse(cur[i], prop + "[" + i + "]");
	            if (l == 0)
	                result[prop] = [];
	        } else {
	            var isEmpty = true;
	            for (var p in cur) {
	                isEmpty = false;
	                recurse(cur[p], prop ? prop+"."+p : p);
	            }
	            if (isEmpty && prop)
	                result[prop] = {};
	        }
	    }
	    recurse(data, "");
	    return result;
	}
	function unflatten(data) {
	    "use strict";
	    if (Object(data) !== data || Array.isArray(data))
	        return data;
	    var regex = /\.?([^.\[\]]+)|\[(\d+)\]/g,
	        resultholder = {};
	    for (var p in data) {
	        var cur = resultholder,
	            prop = "",
	            m;
	        while (m = regex.exec(p)) {
	            cur = cur[prop] || (cur[prop] = (m[2] ? [] : {}));
	            prop = m[2] || m[1];
	        }
	        cur[prop] = data[p];
	    }
	    return resultholder[""] || resultholder;
	}
	return {
    set: function(data) {
    	angular.forEach(flatten(data),function(value,key){$location.search(key, value);});
    },

    get: function() {
      return unflatten($location.search());
    }

  };
})
 .service('cartService', function($rootScope,$http) {
	 return {
		 setSamples: setSamples,
		 getSamples: getSamples,
		 removeSamples: removeSamples,
		 addSamples: addSamples
	 };
	 var samples = [];
	 function setSamples(data) {
		 samples = data;
		 $rootScope.$broadcast('cart',data);
	 }

	 function getSamples(){
		 console.log('get',samples);
		 return samples;
	 }
	 function removeSamples(sample_ids){
		 var url = django_js_utils.urls.resolve('remove_samples_from_cart');
		 $http.post(url,{sample_ids:sample_ids})
		 .success(function(data, status, headers, config) {
			 setSamples(data);
		 }).error(function(){
		 });
	 };
	 function addSamples(sample_ids){
		 var url = django_js_utils.urls.resolve('add_samples_to_cart');
		 $http.post(url,{sample_ids:sample_ids})
		 .success(function(data, status, headers, config) {
			 setSamples(data);
		 }).error(function(){
		 });
	 };


 })
.service('urlService', function($rootScope,$http) {
	 return {
		 getURL: getURL
	 };
	 function getURL(name,params) {
		 return django_js_utils.urls.resolve(name, params);
	 }


});
//$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab.id })};

