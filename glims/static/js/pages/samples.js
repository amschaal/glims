
angular.module('Dashboard')
.controller('SampleController', ['$scope', SampleController]);

function SampleController($scope) {
	$scope.headers=[{'name':'name','label':'Name'},{'name':'project','label':'Project','order_by':'project__name'},{'name':'description','label':'Description'}];
	$scope.permissionLink = function(sample){return django_js_utils.urls.resolve('permissions', { model: 'sample', pk: sample.id })};
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	$scope.projectLink = function(sample){return django_js_utils.urls.resolve('project', { pk: sample.project })};
}

