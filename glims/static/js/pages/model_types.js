
angular.module('mainapp')
.controller('ModelTypesController', ['$scope','DRFNgTableParams', ModelTypesController]);

function ModelTypesController($scope,DRFNgTableParams) {
	$scope.headers=[{'name':'content_type__name','label':'Content Type'},{'name':'name','label':'Name','order_by':'name'},{'name':'description','label':'Description'}];
	$scope.link = function(id){return django_js_utils.urls.resolve('model_type', { pk: id })};
	$scope.tableParams = DRFNgTableParams('/api/model_types/',{sorting: { content_type__name: "asc" }});
	
	
}

