
angular.module('mainapp')
.controller('RunsController', ['$scope','$http','DRFNgTableParams', RunsController]);

function RunsController($scope,$http,DRFNgTableParams) {
	var defaults={};
	$scope.tableParams = DRFNgTableParams('/sequencing/api/runs/',{sorting: { created: "desc" }});
}