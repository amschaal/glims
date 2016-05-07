
var app = angular.module('mainapp');
app.requires.push('ui.grid','ui.grid.pinning','ui.grid.resizeColumns','glims.formly');
app.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}])
.controller('ProjectController', ['$scope','$log','$http','FormlyModal', 'ModelType', 'Project','projectService','Subscription',ProjectController])
function ProjectController($scope , $log, $http, FormlyModal, ModelType, Project, projectService, Subscription){
	$scope.init = function (params){
		$scope.project_id = params.project;
		$scope.project = Project.get({id:params.project});
//		$scope.subscription = Subscription.get({object_id:params.project,content_type__model:'project'});
		
	};
	$scope.editProject = function(){
		projectService.update($scope.project)
		.result.then(
				function (project) {
				    $scope.project = project;
				}
				);
	}
	$scope.deleteProject = function(){
		if (!confirm('Are you sure you want to delete this project?  This action cannot be undone!'))
			return;
		$scope.project.$delete(function(){window.location.href = $scope.getURL('projects');})
	}
//	$http.get('/plugins/api/get_plugins/').then(function(response){console.log('plugin data',response.data);$scope.plugins=response.data});
	
	$scope.sample_plugin = "<samples-plugin project='project' ng-if='project.id'></samples-plugin>";
//	$scope.sample_plugin = '<h2>Test</h2>';

}

