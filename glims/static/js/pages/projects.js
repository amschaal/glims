
var app = angular.module('mainapp');
app.requires.push('glims.formly');
app.controller('ProjectController', ['$scope','$http','DRFNgTableParams','FormlyModal', 'Project','projectService', ProjectController]);

function ProjectController($scope,$http,DRFNgTableParams, FormlyModal, Project,projectService) {
	var defaults={};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab.id })};
	$scope.requestParams = {sorting: { created: "desc" },filter:{archived:'False',following:true}}
	$scope.cols = {'Created':true,'ID':true,'Name':true,'Type':true,'Group':false,'Lab':true,'Manager':true,'Participants':false,'Description':true,'Status':true}
	$scope.tableParams = DRFNgTableParams('/api/projects/',$scope.requestParams ,Project);
	$scope.tableParams;
	$scope.userProfile.$promise.then(function(profile){
		console.log('profile',profile);
		if (_.has(profile,'preferences.pages.projects.requestParams.filter')){
			$scope.requestParams.filter = profile.preferences.pages.projects.requestParams.filter;
			$scope.updateFilters();
		}
	});
	$scope.saveFilters = function(){
		_.set($scope.userProfile,'preferences.pages.projects.requestParams.filter',$scope.requestParams.filter)
		$scope.userProfile.$save();
	}
	$scope.changeFilter = function(field, value){
	      var filter = {};
	      filter[field] = value;
	      angular.extend($scope.tableParams.filter(), filter);
	    }
	$scope.updateFilters = function(){
		console.log('filter',$scope.requestParams.filter)
		$scope.tableParams.filter($scope.requestParams.filter);
	}
	$scope.saveStatus = function(project){
		console.log('project',project);
		project.status = project.new_status.id;
	}
	
	$scope.createProject = function(){
		projectService.create();
	}
}