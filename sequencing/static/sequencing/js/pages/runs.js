
angular.module('mainapp')
.controller('RunController', ['$scope','$http','DRFNgTableParams', RunController]);

function RunController($scope,$http,DRFNgTableParams) {
	var defaults={};
	$scope.tableParams = DRFNgTableParams('/sequencing/api/runs/',{sorting: { created: "desc" }});
}