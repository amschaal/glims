angular.module('mainapp')
.controller('SampleModalController', function SampleModalController($scope, $http, DRFNgTableParams, $modalInstance,addFunc,scope) {
	$scope.addFunc = addFunc;
	$scope.scope = scope;
	$scope.permissionLink = function(sample){return django_js_utils.urls.resolve('permissions', { model: 'sample', pk: sample.id })};
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	$scope.projectLink = function(sample){return django_js_utils.urls.resolve('project', { pk: sample.project })};
	$scope.tableParams = DRFNgTableParams('/api/samples/',{sorting: { created: "desc" }});
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
