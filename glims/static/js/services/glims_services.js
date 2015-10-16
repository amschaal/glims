angular.module('glimsServices',['ngTable'])
.factory('DRFNgTableParams', ['NgTableParams','$http', function(NgTableParams,$http) {
	   return function(url,ngparams) {
		   var params = {
//				    page: 1, // show first page
				    count: 10 // count per page
				  }
		   angular.merge(params,ngparams);
		   return new NgTableParams(params, {
			    filterDelay: 0,
				  	getData: function(params) {
				  		var url_params = params.url();
				  		console.log(params);
				  		console.log(url);
				  	var query_params = {page:url_params.page,page_size:url_params.count,ordering:params.orderBy().join(',').replace('+','')};
				  	angular.extend(query_params, params.filter());
			      // ajax request to api
				  	return $http.get(url,{params:query_params}).then(function(response){
				  		console.log(response.data);
				  		params.total(response.data.count);
				  		return response.data.results;
				  	});
			    }
			  });
	   };
	 }]);
