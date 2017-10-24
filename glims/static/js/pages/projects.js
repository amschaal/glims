
var app = angular.module('mainapp');
app.requires.push('glims.formly','project');
app.controller('ProjectController', ['$scope','$http','DRFNgTableParams','FormlyModal', 'Project','ModelType','projectService','growl', ProjectController]);

function ProjectController($scope,$http,DRFNgTableParams, FormlyModal, Project,ModelType,projectService,growl) {
	var defaults={};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab.id })};
	$scope.tableSettings = {sorting: { created: "desc" },filter:{archived:'False',following:true}}
	$scope.cols = {'Created':true,'Modified':true,'ID':true,'Name':true,'Type':true,'Group':false,'Lab':true,'Manager':true,'Participants':false,'Description':true,'Contact':false,'Status':true,'Archived':false,'Subscription':false}
	$scope.types = ModelType.query({content_type__model:'project'});
	$scope.userProfile.$promise.then(function(profile){
		console.log('profile',profile);
		if (_.has(profile,'preferences.pages.projects.tableSettings.filter'))
			$scope.tableSettings.filter = profile.preferences.pages.projects.tableSettings.filter;
		if (_.has(profile,'preferences.pages.projects.tableSettings.sorting'))
			$scope.tableSettings.sorting = profile.preferences.pages.projects.tableSettings.sorting;
		if (_.has(profile,'preferences.pages.projects.tableSettings.cols'))
			angular.extend($scope.cols,profile.preferences.pages.projects.tableSettings.cols);
//		if (_.has(profile,'preferences.pages.projects.tableSettings.sorting')){
//				$scope.tableSettings.sorting = profile.preferences.pages.projects.tableSettings.filter;
		$scope.tableParams = DRFNgTableParams('/api/projects/',$scope.tableSettings ,Project);
	});
	$scope.saveFilters = function(){
		_.set($scope.userProfile,'preferences.pages.projects.tableSettings.filter',$scope.tableParams.filter());
		_.set($scope.userProfile,'preferences.pages.projects.tableSettings.sorting',$scope.tableParams.sorting());
		_.set($scope.userProfile,'preferences.pages.projects.tableSettings.cols',$scope.cols);
		$scope.save_disabled = true;
		$scope.saveProfileText = 'Saving...';
		$scope.userProfile.$save(
			function(){$scope.save_disabled=false;$scope.saveProfileText = null;growl.success("Savings saved",{ttl: 3000})},
			function(){$scope.save_disabled=false;$scope.saveProfileText = null;growl.error("Error saving settings",{ttl: 3000})}
		);
	}
	$scope.changeFilter = function(field, value){
	      var filter = {};
	      filter[field] = value;
	      angular.extend($scope.tableParams.filter(), filter);
	    }
	$scope.updateFilters = function(){
		console.log('filter',$scope.tableSettings.filter)
		$scope.tableParams.filter($scope.tableSettings.filter);
	}
	$scope.saveStatus = function(project){
		console.log('project',project);
		project.status = project.new_status.id;
	}
	
	$scope.createProject = function(){
		projectService.create();
	}
}