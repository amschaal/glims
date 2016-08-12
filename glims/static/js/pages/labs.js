
angular.module('mainapp')
.controller('LabController', ['$scope','DRFNgTableParams', LabController]);

function LabController($scope,DRFNgTableParams) {
	$scope.labLink = function(lab){return django_js_utils.urls.resolve('lab',{pk:lab.id});};
	$scope.projectsLink = function(lab){return django_js_utils.urls.resolve('projects')+"?lab__name="+lab.name;};
	$scope.samplesLink = function(lab){return django_js_utils.urls.resolve('samples')+"?project__lab__name="+lab.name;};
	$scope.tableParams = DRFNgTableParams('/api/labs/',{sorting: { last_name: "asc" }});
}

