angular.module("tracker-plugin");

angular.module('plugins').requires.push("tracker-plugin");

angular.module("tracker-plugin")
.directive('trackerLogs', function(Log,Category) {
	return {
		restrict: 'AE',
		templateUrl: 'template/tracker/logs.html',
		scope: {
			projectId:'=',
			statuses:'='
		},
		controller: function ($scope,$rootScope) {
			$scope.logs = [];
			$scope.deleteLog = function(index){
				if (!$scope.logs[index].id)
					$scope.logs.splice(index,1);
				else {
					if (!confirm("Are you sure you want to delete this log?"))
						return;
					$scope.logs[index].$remove(function(){
						$scope.logs.splice(index,1);
					});
				}
			};
			$scope.editLog = function(log){
				log.editing = true;
			};
			$scope.save = function(log){
				if(log.id)
					log.$save(function(){},function(response){log.errors = response.data;});
				else
					log.$create(function(){},function(response){log.errors = response.data;});
			};
			$scope.newLog = function(){
				var log = new Log({project:$scope.projectId});
				log.editing=true;
				$scope.logs.push(log);
			};
			$scope.init = function(){
				$scope.$watch('projectId',function(projectId,oldValue){
					if (!projectId)
						return;
					$scope.logs = Log.query({project:projectId},function(){});
					$scope.categories = Category.query({project:projectId},function(){});
				});
			};
			$scope.total = function(){
				return _.sumBy($scope.logs, function(o) { return o.quantity ? parseFloat(o.quantity) : 0; });
			}
			
			
		}
	}
});

angular.module("tracker-plugin").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/tracker/logs.html',
	'<load-on-select><div ng-init="init()">\
	<h4 ng-if="!logs.length">There are currently no Logs.</h4>\
	<table class="table" ng-if="logs.length">\
	<tr class="no-border-top"><th>User</th><th>Category</th><th>Quantity</th><th>Description</th><th>Status</th><th>Exports</th><td></td></tr>\
	<tr ng-repeat="log in logs">\
	<td>{[log.user.first_name]} {[log.user.last_name]}</td>\
	<td ng-if="!log.editing">{[log.category.name]}</span></td>\
	<td ng-if="log.editing">\
			<p class="error" ng-repeat="error in log.errors.category">{[error]}</p>\
			<select ng-options="c.id as c.name for c in categories track by c.id" ng-model="log.category" class="form-control"></select>\
	</td>\
	<td ng-if="!log.editing">\
			{[log.quantity]}\
	</td>\
	<td ng-if="log.editing" style="width:30px">\
			<p class="error" ng-repeat="error in log.errors.quantity">{[error]}</p>\
			<input ng-model="log.quantity" size="4" class="form-control"/>\
	</td>\
	<td ng-if="!log.editing">{[log.description]}</td><td ng-if="log.editing"><textarea ng-model="log.description" class="form-control"></textarea></td>\
	<td ng-if="log.editing">\
		<p class="error" ng-repeat="error in log.errors.status">{[error]}</p>\
			<select ng-options="key as value for (key,value) in statuses" ng-model="log.status" class="form-control"></select>\
	</td>\
	<td ng-if="!log.editing">{[log.status]}</td>\
	<td><a href="/tracker/exports/#/exports/{[e.id]}/" ng-repeat="e in log.exports" title="{[e.description]}">{[e.created|date]}<span ng-repeat-end ng-if="!$last">, </span></a></td>\
	<td>\
		<button class="btn btn-xs btn-danger pull-right" ng-click="deleteLog($index)">Delete</button>\
		<button class="btn btn-xs pull-right" ng-if="!log.editing" ng-click="editLog(log)">Edit</button>\
		<button class="btn btn-xs btn-success pull-right" ng-if="log.editing" ng-click="save(log)">Save</button>\
	</td>\
	</tr>\
	</table>\
	<label>Totals:</label> {[total()]}\
	<br><button ng-click="newLog()" class="btn btn-success">New Log</button>\
	</div></load-on-select>'
	);
}]);


