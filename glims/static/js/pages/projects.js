
var app = angular.module('mainapp');
app.requires.push('glims.formly');
app.controller('ProjectController', ['$scope','$http','DRFNgTableParams','FormlyModal', 'Project', 'ModelType', ProjectController]);

function ProjectController($scope,$http,DRFNgTableParams, FormlyModal, Project, ModelType) {
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
	var sample_types = ModelType.query({content_type__model:'sample'});
	$scope.createProject = function () {
		var fields =  [

//						{
//							  key: 'status',
//							  type: 'select',
//							  templateOptions: {
//							    label: 'Status',
////							    ngOptions: "option as option.name for option in row.status_options track by option.id",
//							    options: $scope.project.status_options,
//							    valueProp: 'id',
//							    labelProp: 'name'
//							  }
//						},
						{"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"
						}, 
		                 {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"
		                 },
		                 {
		                	  key: 'sample_type',
		                	  type: 'select',
		                	  templateOptions: {
		                	    label: 'Sample Type',
		                	    ngOptions: "option as option.name for option in to.options track by option.id",
		                	    options: sample_types,
		                	    valueProp: 'id',
		                	    labelProp: 'name'
		                	  }
		                 },
		                 {
	                     key: 'lab',
	                     type: 'ui-select-search',
	                     templateOptions: {
	                       optionsAttr: 'bs-options',
	                       label: 'Lab',
	                       valueProp: 'id',
	                       labelProp: 'name',
	                       url: '/api/labs/',
	                       options: []
	                     }
	                   }
	                	];
    	FormlyModal.create(fields,new Project({}),{model_type_query:{content_type__model:'project'},title:'Create project',controller:'ExtendedFormlyModalController'})
    	.result.then(
    			function (project) {
//    		    	$scope.project = project;
    				window.location.href=$scope.getURL('project',{pk:project.id});
    		    }
    	);
    	
    };
}