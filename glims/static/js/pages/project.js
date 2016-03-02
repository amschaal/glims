
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
.controller('ProjectController', ['$scope','$log','FormlyModal', 'ModelType', 'Project','projectService',ProjectController])
.controller('SamplesController', ['$scope','$http','$log','$uibModal','Sample','sampleService', SamplesController]);
function ProjectController($scope , $log, FormlyModal, ModelType, Project, projectService){
	$scope.init = function (params){
		$scope.project_id = params.project;
		$scope.project = Project.get({id:params.project});
	};
	
//	var sample_types = ModelType.query({content_type__model:'sample'});
	$scope.editProject = function(){
		projectService.update($scope.project)
		.result.then(
				function (project) {
				    $scope.project = project;
				}
				);
	}
//	$scope.editProject = function () {
//		var fields =  [
//
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
//						{"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"
//						}, 
//		                 {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"
//		                 },
//		                 {
//		                	  key: 'sample_type',
//		                	  type: 'select',
//		                	  templateOptions: {
//		                	    label: 'Sample Type',
//		                	    ngOptions: "option as option.name for option in to.options track by option.id",
//		                	    options: sample_types,
//		                	    valueProp: 'id',
//		                	    labelProp: 'name'
//		                	  }
//		                 },
//		                 {
//	                     key: 'lab',
//	                     type: 'ui-select-search',
//	                     templateOptions: {
//	                       optionsAttr: 'bs-options',
//	                       label: 'Lab',
//	                       valueProp: 'id',
//	                       labelProp: 'name',
//	                       url: '/api/labs/',
//	                       options: []
//	                     }
//	                   }
//	                	];
//    	FormlyModal.create(fields,$scope.project,{model_type_query:{content_type__model:'project'},title:'Edit project',controller:'ExtendedFormlyModalController'})
//    	.result.then(
//    			function (project) {
//    		    	$scope.project = project;
//    		    }
//    	);
//    	
//    };
}
function SamplesController($scope,$http,$log,$uibModal,Sample,sampleService) {
	$scope.errors = false;
	$scope.save = function(sample){
		$log.info('save',sample);
		var onSuccess = function(response){delete sample.errors;};
		var onError = function(response){sample.errors = response.data;$log.info(response.data);};
		if(sample.id)
			sample.$save(onSuccess,onError);
		else
			sample.$create(onSuccess,onError);
	};
	$scope.cancel = function(sample,index){
		sample.editing=false;
		if(!sample.id)
			$scope.samples.splice(index,1);
	};
	$scope.deleteSample = function(row,index){
		index = $scope.gridOptions.data.indexOf(row.entity);
		$log.info(row,index);
		if (row.entity.id){
			if (confirm("Are you sure you want to delete this sample and all associated data?"))
				row.entity.$remove(function(){$scope.gridOptions.data.splice(index,1);});
		}else{
			$scope.gridOptions.data.splice(index,1);
		}

	};
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	$scope.uploadFile = function(url){
        var file = $scope.myFile;
        $log.info('file is ' );
        console.dir(file);
        
        var fd = new FormData();
//        if ($scope.merge)
//        	fd.append('merge', true);
        fd.append('tsv', file);

        $http.post(url, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(data){
        	$scope.errors = false;
        	$scope.refreshSamples();
        })
        .error(function(data){
        	$log.info('errors',data)
        	$scope.errors = data.errors;
        });
        
    };
	$scope.init = function(){
		$scope.refreshSamples();
	};
	$scope.refreshSamples = function(){
		$scope.samples = Sample.query({project:$scope.project_id},function() {
			$scope.gridOptions.data = $scope.samples;
		});
	}
	var columnDefs = [
	                  {
	                	  	displayName: "Actions",
	                	  	name: 'actions',
						    cellTemplate: '\
						    	<span uib-dropdown dropdown-append-to-body on-toggle="toggled(open)">\
						        <a href id="simple-dropdown" uib-dropdown-toggle>\
					        Actions<span class="caret"></span>\
					      </a>\
					      <ul class="uib-dropdown-menu" aria-labelledby="simple-dropdown">\
					        <li>\
						    	<a ng-click="grid.appScope.edit_sample(row)">Modify</a>\
						    	<a ng-click="grid.appScope.deleteSample(row,$index)">Delete</a>\
					        </li>\
					      </ul>\
					    </span>',
						    pinnedLeft:true,
						    width:80,
						    enableSorting: false,
						    enableColumnMenu: false,
						    enableFiltering: false
	                  },
	                  {displayName: "ID", name: "sample_id", pinnedLeft:true, minWidth: 150},
	                  {displayName: "Type", name: "type.name", minWidth: 150,
	                	  cellTemplate: '<div class="ui-grid-cell-contents" ng-class="{\'error\':grid.appScope.project.sample_type.id != row.entity.type.id}">{{COL_FIELD}}</div>'
	                  },
	                  {displayName: "Name", name: "name", minWidth: 150},
	                  {displayName: "Description", name: "description", minWidth: 150},
	                  {displayName: "Received", name: "received", minWidth: 150, type:'date'},
	                  
	              ];
	$scope.$watch('project.sample_type',function(newValue,oldValue){
		if (!$scope.project.sample_type)
			return;
		var cols = angular.copy(columnDefs);
		angular.forEach($scope.project.sample_type.fields,function(field){
			cols.push({
				displayName:field.label,
				name:'data.'+field.name,
				minWidth: 100,
				cellTemplate: '<div class="ui-grid-cell-contents"><div ng-if="grid.appScope.project.sample_type.id != row.entity.type.id" class="error">Incompatible type!</div>{{COL_FIELD}}</div>'
			});
		});
		$scope.gridOptions.columnDefs = cols;
	});
	
	
	

	  $scope.gridOptions = {
	      columnDefs: columnDefs,
	      onRegisterApi: function(gridApi){
	          $scope.gridApi = gridApi;
	      },
	      showGridFooter: true,
	      enableFiltering: true
	  };

	    $scope.edit_sample = function(row){
	    	var sample = row ? row.entity : new Sample({project:$scope.project.id,type:$scope.project.sample_type,data:{}});
			sampleService.update(sample)
			.result.then(
					function (updatedSample) {
						if (row)
	    		    		row.entity = updatedSample;
	    		    	else
	    		    		$scope.samples.push(updatedSample);
					}
					);
		}
	
}

