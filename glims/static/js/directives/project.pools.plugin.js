
angular.module("project-pools-plugin", ['glims.formly','glimsModels','glimsServices','ngTable']);

angular.module('plugins').requires.push("project-pools-plugin")

angular.module("project-pools-plugin")
.directive('projectPools', function(Sample,Project,Pool,poolService) {
	return {
		restrict: 'AE',
		templateUrl: 'template/plugins/project_pools.html',
		scope: {
			project:'=',
//			getURL:'&'
		},
		controller: function ($scope,$rootScope,$http,$log,$uibModal,NgTableParams) {
			console.log('pools');
			$scope.getURL = $rootScope.getURL;
			$scope.errors = false;
			$scope.selection = {};
			function updateCount(){
				$rootScope.sample_count = $scope.samples ? $scope.samples.length : 0;
				$rootScope.pool_count = $scope.pools ? $scope.pools.length : 0;
			}
			$scope.refresh = function(){
				console.log('refreshing samples',$scope.sample);
				$scope.samples = Sample.query({project__id:$scope.project.id,page_size:100},function() {
//					$scope.tableParams = new NgTableParams({}, {
//					      dataset: $scope.samples
//					    });
					updateCount();
				});
				$scope.pools = Pool.query({libraries__sample__project__id:$scope.project.id,page_size:100},function() {
					updateCount();
				});
			}
			$scope.$watch('project.id',function(newValue,oldValue){
				if (newValue)
					$scope.refresh();
			});
			$scope.createPool = function(){
				poolService.create(new Pool({name:$scope.project.name})).result.then(
						function(pool){
							console.log('pool',pool);$scope.pools.push(pool);
						});
			}
		}

	}
});


angular.module("project-pools-plugin").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/plugins/project_pools.html',
			'<load-on-select>\
			<div class="row">\
			<div class="col-md-6">\
			<div ng-repeat="sample in samples"><label><input type="checkbox" checklist-model="selection.samples" checklist-value="sample.id"/> {[sample.name]}</label></div>\
			</div>\
			<div class="col-md-6">\
			<h3>Pools <span class="pull-right"><button ng-click="createPool()" class="btn btn-primary">Create</button></span></h3>\
			<uib-accordion><div ng-repeat="pool in pools" uib-accordion-group heading="{[pool.name]}"></div></uib-accordion>\
			</div>\
			</div>\
			{[selection]}\
			</load-on-select>'
	);
}]);

