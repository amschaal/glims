
var app = angular.module('mainapp');
app.requires.push('glims.formly');
app.controller('ProjectController', ['$scope','$http','DRFNgTableParams','FormlyModal', 'Project','projectService', ProjectController]);

function ProjectController($scope,$http,DRFNgTableParams, FormlyModal, Project,projectService) {
	var defaults={};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab.id })};
	$scope.tableParams = DRFNgTableParams('/api/projects/',{sorting: { created: "desc" }});
//	scope.$watch('name', function(newValue, oldValue) {
//		  scope.counter = scope.counter + 1;
//		});
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