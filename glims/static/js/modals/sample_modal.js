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
)
.run(['$templateCache', function($templateCache) {
	$templateCache.put('sampleModal.html',
	'<div class="modal-header"><h3 class="modal-title">Search Samples</h3></div><div class="modal-body"><table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed"><tr ng-repeat="row in $data track by row.id"><td data-title="\'Created\'" sortable="\'created\'"">{[row.created|date]}</td><td data-title="\'ID\'" sortable="\'sample_id\'" filter="{sample_id__icontains: \'text\'}"><a target="_blank" href="{[ sampleLink(row) ]}">{[row.sample_id]}</a></td><td data-title="\'Type\'" sortable="\'type__name\'" filter="{type__name__icontains: \'text\'}">{[row.type__name]}</td><td data-title="\'Project\'" sortable="\'project__name\'" filter="{project__name__icontains: \'text\'}"><a target="_blank" href="{[ projectLink(row) ]}">{[row.project__name]}</a></td><td data-title="\'Description\'" sortable="\'description\'" filter="{description__icontains: \'text\'}">{[row.description]}</td><td><a class="btn btn-xs btn-success" ng-hide="exists(row)" ng-click="addFunc(row)">Add</a> </td></tr></table></div><div class="modal-footer"><button class="btn btn-warning" ng-click="dismiss()">Dismiss</button></div>'
    );
}]);