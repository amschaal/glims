
angular.module('mainapp')
.controller('PoolController', ['$scope','$http', PoolController]);

function PoolController($scope,$http) {
	$scope.print = function(){console.log('pool',$scope.pool)};
	$scope.errors={};
	$scope.getErrors = function(name){
		return $scope.errors[name] ? $scope.errors[name] : []; 
	};
	$scope.submit = function(){
		var url = django_js_utils.urls.resolve('update_pool', { pk: 6});
		$http.post(
			url,
			$scope.pool
		).success(function(data, status, headers, config) {
			console.log('data',data);
			if (data.errors)
				$scope.errors=data.errors;
			else
				$scope.errors={};
		});
	}
	
}


angular.module('mainapp')
.controller('SamplesController', ['$scope','Sample', SamplesController]);

function SamplesController($scope,$Sample) {
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	$scope.init = function(samples){
		console.log('samples',samples);
		$scope.samples = samples
	};
	
	
	
}

