
angular.module('mainapp')
.controller('ProjectController', ['$scope','DRFNgTableParams','Project','projectService', ProjectController])
.controller('SampleController', ['$scope','$http','DRFNgTableParams','cartService', SampleController]);
function ProjectController($scope,DRFNgTableParams,Project,projectService) {
	$scope.permissionLink = function(project){return django_js_utils.urls.resolve('permissions', { model: 'project', pk: project.id })};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.createProject = function(){
		projectService.create(new Project({lab:$scope.lab_id}),{exclude:['lab']});
	}
	$scope.init = function(filters,lab_id){
		$scope.lab_id = lab_id;
		$scope.tableParams = DRFNgTableParams('/api/projects/',{sorting: { created: "desc" },filter:filters});
	}
}


function SampleController($scope, $http,DRFNgTableParams, cartService) {
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	$scope.projectLink = function(sample){return django_js_utils.urls.resolve('project', { pk: sample.project })};
	$scope.init = function(filters){
		$scope.tableParams = DRFNgTableParams('/api/samples/',{sorting: { created: "desc" },filter:filters});
	}
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