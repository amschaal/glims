
angular.module('mainapp')
.controller('ModelTypesController', ['$scope', ModelTypesController]);

function ModelTypesController($scope) {
	$scope.headers=[{'name':'content_type','label':'Content Type'},{'name':'name','label':'Name','order_by':'name'},{'name':'description','label':'Description'}];
	$scope.link = function(id){return django_js_utils.urls.resolve('model_type', { id: id })};
	
	
	
}

