angular.module('glimsServices',['ngTable'])
.factory('DRFNgTableParams', ['NgTableParams','$http', function(NgTableParams,$http) {
	return function(url,ngparams) {
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
}])
 .service('cartService', function($rootScope,$http) {
	 return {
		 setSamples: setSamples,
		 getSamples: getSamples,
		 removeSamples: removeSamples,
		 addSamples: addSamples
	 };
	 var samples = [];
	 function setSamples(data) {
		 console.log('set',data);
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


 });

