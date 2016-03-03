
angular.module('glims.samplecart',[])
.controller('CartMenuController', ['$scope','$http','cartService', CartMenuController]);

function CartMenuController($scope,$http,cartService) {
	$scope.samples=[1];
	$scope.$on('cart',function (event, data) {
	    $scope.samples = cartService.getSamples();
	  });
	$scope.init = function(){
		console.log('init cart');
		var url = django_js_utils.urls.resolve('add_samples_to_cart');
		$http.post(url,{sample_ids:[]})
		.success(function(data, status, headers, config) {
			cartService.setSamples(data);
		}).error(function(){
		});
	}
	$scope.Utils= {
		     keys : Object.keys
    }
}

