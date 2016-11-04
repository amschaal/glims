//angular.module("plugin-base",[])
//.directive('plugin',function(){
//	return {
//		controller: function($scope,$rootScope){
//			alert('wtf');
//			$scope.getURL = $rootScope.getURL;
//		}
//	}
//});



angular.module("samples-plugin", ['ui.grid','ui.grid.edit','ui.grid.pinning','ui.grid.resizeColumns','glims.formly']);
//angular.module("samples.tpls", ["template/plugins/samples.html"]);

angular.module('plugins').requires.push("samples-plugin")

angular.module("samples-plugin")
.directive('samplesPlugin', function(Sample,sampleService) {
	return {
		restrict: 'AE',
		templateUrl: 'template/plugins/samples.html',
		scope: {
//			objectId:'@',
//			contentType:'@',
			project:'=',
			getURL:'&',
			data: '='
		},
		controller: function ($scope,$rootScope,$http,$log,$uibModal) {
			$scope.getURL = $rootScope.getURL;
			$scope.data = {};
			$scope.errors = false;
			function updateSampleCount(){
				$rootScope.sample_count = $scope.samples ? $scope.samples.length : 0;
			}
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
						row.entity.$remove(function(){
							$scope.gridOptions.data.splice(index,1);
							updateSampleCount();
						});
				}else{
					$scope.gridOptions.data.splice(index,1);
					updateSampleCount()
				}

			};
			$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
			$scope.uploadFile = function(url){
				var file = $scope.data.file;
				$log.info('file is ' );
				console.dir(file);

				var fd = new FormData();
//				if ($scope.merge)
//				fd.append('merge', true);
				fd.append('sheet', file);

				$http.post(url, fd, {
					transformRequest: angular.identity,
					headers: {'Content-Type': undefined}
				})
				.success(function(data){
					$scope.errors = false;
					$scope.refreshSamples();
				})
				.error(function(data){
					$log.info('errors',data);
					$scope.errors = data.errors;
				});

			};
			$scope.clearErrors = function(){
				$scope.errors = false;
			}
			$scope.refreshSamples = function(){
				$scope.samples = Sample.query({project:$scope.project.id,page_size:1000},function() {
					$scope.gridOptions.data = $scope.samples;
					console.log($scope.gridOptions);
					updateSampleCount()
//					$scope.gridApi.core.refresh(); //gridApi
				});
			}
			var columnTypes = {'checkbox':'boolean','float':'number','integer':'number'}
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
			                		  enableFiltering: false,
			                		  enableCellEdit: false
			                  },
			                  {displayName: "ID", name: "sample_id", pinnedLeft:true, minWidth: 150,enableCellEdit: false,
			                	cellTemplate:   '<div class="ui-grid-cell-contents"><a href="{[grid.appScope.getURL(\'sample\',{pk:row.entity.id})]}">{{COL_FIELD}}</a></div>'
			                  },
			                  {displayName: "Type", name: "type.name", minWidth: 150,enableCellEdit: false,
			                	  cellTemplate: '<div class="ui-grid-cell-contents" ng-class="{\'error\':grid.appScope.project.sample_type.id != row.entity.type.id}">{{COL_FIELD}}</div>'
			                  },
			                  {displayName: "Name", name: "name", minWidth: 150,enableCellEdit: true},
			                  {displayName: "Description", name: "description", minWidth: 150,enableCellEdit: true},
			                  {displayName: "Received", name: "received", minWidth: 150, type:'date',enableCellEdit: true},

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
						cellTemplate: '<div class="ui-grid-cell-contents"><div ng-if="grid.appScope.project.sample_type.id != row.entity.type.id" class="error">Incompatible type!</div>{{COL_FIELD}}</div>',
						enableCellEdit: true,
						type: columnTypes[field.type] ? columnTypes[field.type] : 'string'
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
			$scope.sampleDownloadURL = function(){
				return $scope.getURL("sample_template") + ($scope.project.sample_type ? '?type_id='+$scope.project.sample_type.id : '');
			}
			$scope.edit_sample = function(row){
				var sample = row ? row.entity : new Sample({project:$scope.project.id,type:$scope.project.sample_type,data:{}});
				sampleService.update(sample)
				.result.then(
						function (updatedSample) {
							if (row)
								row.entity = updatedSample;
							else
								$scope.samples.push(updatedSample);
							updateSampleCount()
						}
				);
			}
			$scope.$watch('project.id',function(newValue,oldValue){
//				alert('watch: '+newValue);
				if (newValue)
					$scope.refreshSamples();
			});
			console.log('plugin scope',$scope);
//			$scope.refreshSamples();
		}

	}
});


angular.module("samples-plugin").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/plugins/samples.html',
			'<load-on-select>\
			<h3>Samples</h3>\
			<div ng-if="project.id">\
			<p>\
			<input type="file" file-model="data.file" style="display:inline-block" /><button ng-click="uploadFile(getURL(\'import_samplesheet\',{project_id:project.id}))" class="btn btn-success">Import samplesheet</button>\
			<br><a href="{[sampleDownloadURL()]}">Download</a> template\
			<a href="{[getURL(\'download_samplesheet\',{project_id:project.id})]}">Download</a> samplesheet\
			</p>\
			<div class="alert alert-danger" role="alert" ng-show="errors">\
				<button ng-click="clearErrors();" class="btn btn-sm btn-danger pull-right">Clear errors</button>\
				<div ng-repeat="(id, sample_errors) in errors">\
					<b>{[id]}:</b>\
					<ul>\
						<li ng-repeat="(id,errors) in sample_errors">\
							{[id]}: {[errors.join(\', \')]}\
						</li>\
					</ul>\
				</div>\
				<div ng-show="errors">There was an error processing the sample file.</div>\
			</div>\
			<div ui-grid="gridOptions" class="grid" ui-grid-pinning ui-grid-resize-columns ui-grid-edit ng-show="samples.length"></div>\
			<button ng-click="edit_sample()" class="btn btn-success">Add sample</button>\
			</div>\
			</load-on-select>'
	);
}]);

