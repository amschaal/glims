
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
.controller('ProjectController', ['$scope','$log','FormlyModal', 'ModelType', 'Project',ProjectController])
.controller('SamplesController', ['$scope','$http','$log','$uibModal','Sample', SamplesController]);
function ProjectController($scope , $log, FormlyModal, ModelType, Project){
	$scope.init = function (params){
		$scope.project = Project.get({id:params.project});
	};
	var fields =  [
						{"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"
						}, 
//		                {"templateOptions": {"required": false, "options": userOptions, "description": "", "label": "Manager","valueProp":"id","labelProp":"first_name" }
//							, "type": "select", "key": "manager.id", data:{"error_key":"manager"}
//						}, 
		                 {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"
		                 },
		                 {
		                	  key: 'sample_type',
		                	  type: 'select',
		                	  templateOptions: {
		                	    label: 'Sample Type',
		                	    options: ModelType.query({}),
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
//	                       labelFunc: function(item,to){return item.first_name + ' ' + item.last_name;},
//	                       placeholder: 'Select lab',
//	                       refresh: refreshUsers,
//	                       refreshDelay: 0
	                       url: '/api/labs/',
	                       options: []
	                     }
	                   }
//		                 {
//		                	  key: 'participants',
//		                	  type: 'objectMultiCheckbox',
//		                	  templateOptions: {
//		                	    label: 'Participants',
//		                	    options: userOptions,
//		                	    valueProp: 'id',
//		                	    labelProp: 'first_name'
//		                	  }
//		                 }
	                	];
	$scope.editProject = function () {
    	FormlyModal.create(fields,$scope.project,{model_type_query:{content_type__model:'project'},title:'Edit project',controller:'ExtendedFormlyModalController'})
    	.result.then(
    			function (project) {
    		    	$scope.project = project;
    		    }
    	);
    	
    };
}
function SamplesController($scope,$http,$log,$uibModal,$Sample) {
	var sampleDefaults;
	$scope.errors = false;
	$scope.setSampleDefaults = function(defaults){
		sampleDefaults = defaults;
		
	};
	$scope.save = function(sample){
		$log.info('save',sample);
		var onSuccess = function(response){delete sample.errors;};
		var onError = function(response){sample.errors = response.data;$log.info(response.data);};
		if(sample.id)
			sample.$save(onSuccess,onError);
		else
			sample.$create(onSuccess,onError);
	};
	$scope.addSample = function(){
//		var sample = new $Sample(sampleDefaults);
//		$scope.samples.push(sample);
//		$log.info('sample',sample);
		$scope.edit_sample();
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
//        	for (var i in data){
//        	var sample = new $Sample(data[i]);
//	    		sample.editing=true;
//	    		$scope.samples.push(sample);	
//        	}
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
		var params = angular.copy(sampleDefaults);
		params.page_size=100;
		$scope.samples = $Sample.query(params,function() {
			angular.forEach($scope.samples,function(sample){
				//$scope.addNote(note);
			});
			$log.info('SAMPLES!',$scope.samples);
			$scope.gridOptions.data = $scope.samples;
		});
	}
	$scope.setFields = function(fields){
		angular.forEach(fields,function(field){
			$scope.gridOptions.columnDefs.push({displayName:field.label,name:'data.'+field.name,minWidth: 100})
		});
	};
	
	var columnDefs = [
	                  {
	                	  	displayName: "Actions",
	                	  	name: 'actions',
						    cellTemplate: '<span uib-dropdown dropdown-append-to-body on-toggle="toggled(open)">\
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
	                  {displayName: "Name", name: "name", minWidth: 150},
	                  {displayName: "Description", name: "description", minWidth: 150},
	                  {displayName: "Received", name: "received", minWidth: 150, type:'date'},
	                  
	              ];

	  $scope.gridOptions = {
	      columnDefs: columnDefs,
	      onRegisterApi: function(gridApi){
	          $scope.gridApi = gridApi;
	      },
	      showGridFooter: true,
	      enableFiltering: true
	  };


	  $scope.edit_sample = function (row) {
		  $log.info(row);
		    var modalInstance = $uibModal.open({
		      templateUrl: 'SampleEdit.html',
		      controller: 'SampleEditCtrl',
		      size: 'lg',
		      resolve: {
		        sample: function () {
		        	if (row)
		        		return angular.copy(row.entity);
		        	else
		        		return new $Sample(sampleDefaults);
		        }
		      }
		    });

		    modalInstance.result.then(function (sample) {
		    	if (row)
		    		row.entity = sample;
		    	else
		    		$scope.samples.push(sample);
		    }, function () {
		      $log.info('Modal dismissed at: ' + new Date());
		    });
		  };
	
}

app.controller('SampleEditCtrl', function ($scope,$log, $uibModalInstance, sample) {
		$log.info(sample);
	  $scope.sample = sample;

	  $scope.ok = function () {
	    $scope.save();
	  };
	  $scope.save = function(){
			$log.info('save',$scope.sample);
			var onSuccess = function(response){delete sample.errors;$uibModalInstance.close(sample);};
			var onError = function(response){sample.errors = response.data;$log.info(response.data);};
			if(sample.id)
				sample.$save(onSuccess,onError);
			else
				sample.$create(onSuccess,onError);
		};
	  $scope.getErrors = function(field){
		  if (!$scope.sample.errors)
			  return [];
		  else
			  return $scope.sample.errors[field];
	  }
	  $scope.cancel = function () {
	    $uibModalInstance.dismiss('cancel');
	  };
	});