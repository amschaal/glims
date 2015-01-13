
angular.module('mainapp')
.controller('CartController', ['$scope','$http','cartService', CartController]);

function CartController($scope,$http,cartService) {
	$scope.$on('cart',function (event, data) {
		console.log('cart!!',data);
	    $scope.samples = cartService.getSamples();
	  });
	$scope.checkAll = function(){
		if($scope.check_all){
			angular.forEach($scope.samples, function(sample, key) {
				  $scope.selectHash[sample.id]=true;
				});
		}else{
			$scope.selectHash={};
		}
	};
	$scope.removeSelected = function(){
		cartService.removeSamples($scope.getSelected());
	};
	$scope.removeAll = function(){
		var sample_ids = []
		angular.forEach($scope.samples, function(sample, key) {
			  sample_ids.push(key);
			});
		cartService.removeSamples($scope.getSelected());
	};
	$scope.getSelected = function(){
		var selected=[];
		angular.forEach($scope.selectHash, function(value, key) {
			  if(value)
				  selected.push(key);
			});
		return selected;
	};
	$scope.selectHash={};
	$scope.removeSample = function(sample){
		cartService.removeSamples([sample.id]);
	};
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	$scope.projectLink = function(sample){return django_js_utils.urls.resolve('project', { pk: sample.project })};

}

