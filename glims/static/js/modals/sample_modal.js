angular.module('mainapp')
.controller('SampleModalController', function SampleModalController($scope, $http, $modalInstance,addFunc,scope) {
	$scope.addFunc = addFunc;
	$scope.scope = scope;
	$scope.headers=[{'name':'name','label':'Name'},{'name':'project','label':'Project','order_by':'project__name'},{'name':'description','label':'Description'}];
	$scope.permissionLink = function(sample){return django_js_utils.urls.resolve('permissions', { model: 'sample', pk: sample.id })};
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	$scope.projectLink = function(sample){return django_js_utils.urls.resolve('project', { pk: sample.project })};
	$scope.exists = function(record){
		for (var i in $scope.scope){
			if ($scope.scope[i].id==record.id)
				return true;
		}
		return false;
	};
  $scope.dismiss = function () {
    $modalInstance.dismiss('cancel');
  };
	
}
);
