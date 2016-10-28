
var app = angular.module('mainapp');
app.requires.push('sequencing');
app.controller('RunController', ['$scope','$log','$http','runService', 'Run',RunController])
function RunController($scope , $log, $http, runService, Run){
	$scope.init = function (params){
		$scope.run = Run.get({id:params.run});
		$scope.editing = false;
		$scope.saved = {};
	};
	$scope.editRun = function(){
		runService.update($scope.run)
		.result.then(
				function (run) {
					$scope.run = run;
				}
		);
	};
	$scope.pools = [];
	$scope.refreshPools = function(pool) {
		console.log('refresh',pool);
		return $http.get('/api/pools/', {params:{search: pool}})
		.then(function(response) {
			$scope.pools = response.data.results;
		});
	};
	$scope.save = function(){
		$scope.run.$save(function(){
			$scope.editing = false;
		});
	};
	$scope.cancel = function(){
		$scope.editing = false;
		angular.copy($scope.saved,$scope.run);
	};
	$scope.edit = function(){
		angular.copy($scope.run,$scope.saved);
		$scope.editing = true;
	};
}
