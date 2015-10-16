
angular.module('mainapp')
.controller('SampleController', ['$scope','$http','cartService','DRFNgTableParams', SampleController]);



function SampleController($scope,$http,cartService,DRFNgTableParams) {
	var defaults={};
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	$scope.projectLink = function(sample){return django_js_utils.urls.resolve('project', { pk: sample.project })};
	$scope.addSample = function(sample){
		cartService.addSamples([sample.id]);
	};
	$scope.removeSample = function(sample){
		cartService.removeSamples([sample.id]);
	};
	$scope.$on('cart',function (event, data) {
	    $scope.cartSamples = cartService.getSamples();
	  });
	$scope.tableParams = DRFNgTableParams('/api/samples/',{sorting: { created: "desc" }});
//		new NgTableParams({
////	      page: 1, // show first page
//	      count: 10 // count per page
//	    }, {
//	      filterDelay: 0,
//		  	getData: function(params) {
//		  		var url = params.url();
//		  		
//		  		console.log(params);
//		  		console.log(url);
//		  	var query_params = {page:url.page,page_size:url.count,ordering:params.orderBy().join(',').replace('+','')};
//		  	angular.extend(query_params, params.filter());
//	        // ajax request to api
//		  	return $http.get('/api/samples/',{params:query_params}).then(function(response){
//		  		console.log(response.data);
//		  		params.total(response.data.count);
//		  		return response.data.results;
//		  	});
//	      }
//	    });
}