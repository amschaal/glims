
angular.module('mainapp').requires.push('sequencing');
angular.module('mainapp')
.controller('RunsController', ['$scope','$http','DRFNgTableParams','runService', RunsController]);

function RunsController($scope,$http,DRFNgTableParams,runService) {
	var defaults={};
	$scope.tableParams = DRFNgTableParams('/sequencing/api/runs/',{sorting: { created: "desc" }});
	$scope.createRun = function(){
		runService.create();
	}
}