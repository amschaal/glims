
angular.module('mainapp')
.controller('ProjectController', ['$scope', ProjectController]);

function ProjectController($scope) {
	$scope.headers=[{'name':'name','label':'Name'},{'name':'type','label':'Type'},{'name':'lab','label':'Lab'},{'name':'description','label':'Description'}];
	$scope.permissionLink = function(project){return django_js_utils.urls.resolve('permissions', { model: 'project', pk: project.id })};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab })};
}

