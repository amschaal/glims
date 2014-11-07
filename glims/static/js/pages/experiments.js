
angular.module('Dashboard')
.controller('ExperimentController', ['$scope', ExperimentController]);

function ExperimentController($scope) {
	$scope.headers=[{'name':'name','label':'Name'},{'name':'description','label':'Description'}];
	$scope.permissionLink = function(experiment){return django_js_utils.urls.resolve('permissions', { model: 'experiment', pk: experiment.id })};
	$scope.experimentLink = function(experiment){return django_js_utils.urls.resolve('experiment', { pk: experiment.id })};
}

