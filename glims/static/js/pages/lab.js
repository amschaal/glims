
angular.module('mainapp')
.controller('ProjectController', ['$scope','DRFNgTableParams','Project','projectService', ProjectController])
.controller('SampleController', ['$scope','$http','DRFNgTableParams','cartService', SampleController])
.controller('LabController', ['$scope','$log', 'Lab','growl',LabController]);
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

function LabController($scope , $log, Lab,growl){
	$scope.init = function (id){
		$scope.id = id;
		$scope.lab = Lab.get({id:id});
	};
	$scope.deleteLab = function(){
		if (!confirm('Are you sure you want to delete this lab?  This action cannot be undone!'))
			return;
		$scope.lab.$delete(function(){window.location.href = $scope.getURL('labs');},function(response){growl.error('Error deleting lab: "'+response.data.detail+'"',{ttl: 10000});})
	}
}