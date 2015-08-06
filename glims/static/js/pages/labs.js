
angular.module('mainapp')
.controller('LabController', ['$scope', LabController]);

function LabController($scope) {
	$scope.headers=[{'name':'name','label':'Name'}];
	$scope.labLink = function(lab){return django_js_utils.urls.resolve('lab',{pk:lab.id});};
	$scope.projectsLink = function(lab){return django_js_utils.urls.resolve('projects')+"?lab__name="+lab.name;};
	$scope.samplesLink = function(lab){return django_js_utils.urls.resolve('samples')+"?project__lab__name="+lab.name;};
//	$scope.experimentsLink = function(lab){return django_js_utils.urls.resolve('experiments')+"?sample__project__lab__name="+lab.name;};
}

