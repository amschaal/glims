
angular.module('mainapp')
.controller('ProjectController', ['$scope', ProjectController])
.controller('SampleController', ['$scope','$http','cartService', SampleController]);
function ProjectController($scope) {
	$scope.headers=[{'name':'name','label':'Name'},{'name':'type','label':'Type'},{'name':'description','label':'Description'}];
	$scope.permissionLink = function(project){return django_js_utils.urls.resolve('permissions', { model: 'project', pk: project.id })};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
}



function SampleController($scope, $http, cartService) {
	$scope.headers=[{'name':'created','label':'Created'},{'name':'name','label':'Name'},{'name':'project','label':'Project','order_by':'project__name'},{'name':'description','label':'Description'}];
	$scope.permissionLink = function(sample){return django_js_utils.urls.resolve('permissions', { model: 'sample', pk: sample.id })};
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	$scope.projectLink = function(sample){return django_js_utils.urls.resolve('project', { pk: sample.project })};
	$scope.addSample = function(sample){
		cartService.addSamples([sample.id]);
	};
	$scope.removeSample = function(sample){
		cartService.removeSamples([sample.id]);
	};
	$scope.$on('cart',function (event, data) {
	    $scope.cartSamples = cartService.getSamples();
	  });
	
}