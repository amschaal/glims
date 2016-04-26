
var app = angular.module('mainapp');
app.requires.push('glims.formly');
app.controller('ProjectController', ['$scope','$http','DRFNgTableParams','FormlyModal', 'Project','projectService', ProjectController]);

function ProjectController($scope,$http,DRFNgTableParams, FormlyModal, Project,projectService) {
	var defaults={};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab.id })};
	$scope.tableParams = DRFNgTableParams('/api/projects/',{sorting: { created: "desc" },filter:{archived:'False'}});
//	scope.$watch('name', function(newValue, oldValue) {
//		  scope.counter = scope.counter + 1;
//		});
	$scope.filterArchive = function(){
		if (!$scope.archived)
			$scope.changeFilter('archived','False');
		else
			delete $scope.tableParams.filter()['archived'];
	}
	$scope.filterGroups = function(){
		var keys = Object.keys($scope.groups);
		var filtered = keys.filter(function(key) {
		    return $scope.groups[key];
		});
		if (filtered.length > 0)
			$scope.changeFilter('group__id__in',filtered.join(','));
		else
			delete $scope.tableParams.filter()['group__id__in'];
	}
	$scope.changeFilter = function(field, value){
	      var filter = {};
	      filter[field] = value;
	      angular.extend($scope.tableParams.filter(), filter);
	    }
	$scope.saveStatus = function(project){
		console.log('project',project);
		project.status = project.new_status.id;
//		if($scope.row.old_status === undefined)
//		$scope.row.old_status = $scope.row.status;
//		$scope.row.status = $scope.row.new_status;
	}
	
	$scope.createProject = function(){
		projectService.create();
	}
}