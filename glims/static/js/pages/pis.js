
angular.module('Dashboard')
.controller('PIController', ['$scope', PIController]);

function PIController($scope) {
	$scope.headers=[{'name':'name','label':'Name'}];
	$scope.studiesLink = function(pi){return django_js_utils.urls.resolve('studies')+"?group__name="+pi.name;};
	$scope.samplesLink = function(pi){return django_js_utils.urls.resolve('samples')+"?study__group__name="+pi.name;};
	$scope.experimentsLink = function(pi){return django_js_utils.urls.resolve('experiments')+"?sample__study__group__name="+pi.name;};
}

