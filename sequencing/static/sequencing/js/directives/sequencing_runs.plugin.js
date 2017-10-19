
angular.module("sequencing-runs-plugin", ['glims.formly','glimsModels','glimsServices','ngTable','sequencing']);

angular.module('plugins').requires.push("sequencing-runs-plugin")

angular.module("sequencing-runs-plugin")
.directive('sequencingRuns', function(Pool,Run) {
	return {
		restrict: 'AE',
		templateUrl: 'template/plugins/sequencing_runs.html',
		scope: {
			pool:'=',
			sample:'=',
		},
		controller: function ($scope,$rootScope,$http,$log,$uibModal,NgTableParams) {
			$scope.getURL = $rootScope.getURL;
			$scope.errors = false;
			function updateRunCount(){
				$rootScope.run_count = $scope.runs ? $scope.runs.length : 0;
			}
			$scope.refreshRuns = function(params){
				
				$scope.runs = Run.query(params,function() {
					$scope.tableParams = new NgTableParams({}, {
					      dataset: $scope.runs
					    });
					updateRunCount();
				});
			}
			$scope.$watch('pool.id',function(newValue,oldValue){
				if (newValue)
					$scope.refreshRuns({'lanes__pool__id':newValue});
			});
			$scope.$watch('sample.id',function(newValue,oldValue){
				if (newValue)
					$scope.refreshRuns({'lanes__pool__library__sample__id':newValue});
			});
		}

	}
});


angular.module("sequencing-runs-plugin").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/plugins/sequencing_runs.html',
			'<load-on-select>\
			<table ng-table="tableParams" class="table table-condensed table-bordered table-striped">\
			<tr ng-repeat="row in $data track by row.id">\
		        <td data-title="\'Created\'" sortable="\'created\'"><a href="{[getURL(\'run\',{pk:row.id})]}">{[row.created|date]}</a></td>\
		        <td data-title="\'Name\'" sortable="\'name\'"><a href="{[getURL(\'run\',{pk:row.id})]}">{[row.name]}</a></td>\
		        <td data-title="\'Machine\'" sortable="\'machine.name\'"><span title="lanes: {[row.machine.num_lanes]}&#010;description: {[row.machine.description]}">{[row.machine.name]}</span></td>\
		        <td data-title="\'Type\'" sortable="\'type__name\'">{[row.type.name]}</td>\
		        <td data-title="\'Pools\'" ><span ng-repeat="l in row.lanes"><a href="{[getURL(\'pool\',{pk:l.pool.id})]}">{[l.pool.name]}</a>{[$last ? \'\' : \', \']}</span></td>\
		        <td data-title="\'Description\'" sortable="\'description\'"><show-more text="row.description" limit="50" lines="1" delimiter="\'\n\'"></show-more></td>\
		      </tr>\
		    </table>\
			</load-on-select>'
	);
}]);

