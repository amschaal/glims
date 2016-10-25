
var app = angular.module('mainapp');
app.requires.push('sequencing');
app.controller('RunController', ['$scope','$log','runService', 'Run',RunController])
function RunController($scope , $log, runService, Run){
	$scope.init = function (params){
		$scope.run = Run.get({id:params.run});
	};
	$scope.editRun = function(){
		runService.update($scope.run)
		.result.then(
				function (run) {
					$scope.run = run;
				}
				);
	}
}
