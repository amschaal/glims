
angular.module('Dashboard')
.controller('PIController', ['$scope', PIController]);

function PIController($scope) {
	$scope.headers=[{'name':'name','label':'Name'}];
	$scope.projectsLink = function(pi){return django_js_utils.urls.resolve('projects')+"?group__name="+pi.name;};
	$scope.samplesLink = function(pi){return django_js_utils.urls.resolve('samples')+"?project__group__name="+pi.name;};
	$scope.experimentsLink = function(pi){return django_js_utils.urls.resolve('experiments')+"?sample__project__group__name="+pi.name;};
}

