
angular.module('mainapp')
.controller('ProjectController', ['$scope','$http','DRFNgTableParams', ProjectController]);

function ProjectController($scope,$http,DRFNgTableParams) {
	var defaults={};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab })};
	$scope.tableParams = DRFNgTableParams('/api/projects/',{sorting: { created: "desc" }});
}