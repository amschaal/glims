
var app = angular.module('mainapp');
app.requires.push('glims.formly');
app.controller('BioinfoProjectController', ['$scope','$http','BioinfoProjectService', 'BioinfoProject','User','FormlyModal', BioinfoProjectController]);

function BioinfoProjectController($scope,$http,BioinfoProjectService,BioinfoProject,User,FormlyModal) {
	$scope.init = function(params){
		console.log(params.id);
		$scope.project = BioinfoProject.get({id:params.id});
		 function refreshUsers(name, field) {
			 console.log(name,field);
			  return  BioinfoProject.users({search:name}).$promise.then(function(users){
				  console.log('users',users);
				  field.templateOptions.options = users;
			  });
           }
		
	};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab })};
	$scope.options = {};	     	    
    
	$scope.editProject = function(){
		BioinfoProjectService.update($scope.project)
		.result.then(
				function (project) {
				    $scope.project = project;
				}
				);
	}
	$scope.deleteProject = function(){
		if (!confirm('Are you sure you want to delete this project?  This action cannot be undone!'))
			return;
		$scope.project.$delete(function(){window.location.href = $scope.getURL('bioinformatics__projects');})
	}
}

