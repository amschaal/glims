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
		controller: function ($scope,$rootScope,NgTableParams,FormlyModal) {
			console.log('statuses',$scope.statuses,_.map($scope.statuses,function(key,val){return {name:val,value:key}}));
			var fields = [];
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
				//log.editing = true;
				console.log('log',log);
				FormlyModal.create(fields,log,{title:'Edit log'}).result.then(function(new_log){//,by_reference:true
					console.log('log',new_log,log);
					log = new_log
					$scope.tableParams.reload();
				});
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
			function configureFields(){
				console.log('categories',$scope.categories,_.map($scope.categories,function(key,val){return {name:val,value:key}}));
				fields = [
								{
								    "key": "quantity",
								    "type": "input",
								    "templateOptions": {
								      "label": "Hours",
								    }
								 },
							     {
								    "key": "status",
								    "type": "select",
								    "templateOptions": {
								      "label": "Status",
								      "options":
								    	  _.map($scope.statuses,function(key,val){return {name:val,value:key}})
								    }
								  },
								  {
								    "key": "category",
								    "type": "select",
								    "templateOptions": {
								      "label": "Category",
								      "options":
								    	  _.map($scope.categories,function(cat){return {name:cat.name,value:cat.id}})
								    }
								  }
							];
			}
			$scope.init = function(){
				$scope.$watch('projectId',function(projectId,oldValue){
					if (!projectId)
						return;
					$scope.logs = Log.query({project:projectId,page_size:10000},function(response){
			    		console.log('logs',response,$scope.logs);
			    		$scope.tableParams = new NgTableParams({}, {
			    		      dataset: $scope.logs
			    		    });
			    	})
//					$scope.logs = Log.query({project:projectId},function(){});
					$scope.categories = Category.query({project:projectId},function(){configureFields();});
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
			<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed">\
		      <tr ng-repeat="row in $data track by row.id">\
		        <td data-title="\'Modified\'" sortable="\'modified\'">{[row.modified|date]}</td>\
				<td data-title="\'Status\'" sortable="\'status\'" filter="{status: \'select\'}" filter-data=\'getStatuses()\'>{[row.status]}</td>\
		        <td data-title="\'Hours\'" sortable="\'quantity\'">{[row.quantity]}</a></td>\
				<td data-title="\'Category\'" sortable="\'category.name\'" filter="{\'category.name\': \'text\'}">{[row.category.name]}</td>\
				<td data-title="\'User\'" sortable="\'user.name\'" filter="{\'user.name\': \'text\'}">{[row.user.name]}</a></td>\
				<td data-title="\'Project\'" sortable="\'project.name\'" filter="{\'project.name\': \'text\'}"><a href="{[getURL(\'project\',{pk:row.project.id})]}">{[row.project.name]}</a></td>\
				<td data-title="\'Lab\'" filter="{\'project.lab\': \'text\'}" sortable="\'project.lab\'">{[row.project.lab]}</td>\
				<td data-title="\'Description\'" filter="{description: \'text\'}">{[row.description]}</td>\
				<td>\
					<button class="btn btn-xs btn-danger pull-right" ng-click="deleteLog($index)">Delete</button>\
					<button class="btn btn-xs pull-right" ng-if="!log.editing" ng-click="editLog(row)">Edit</button>\
					<button class="btn btn-xs btn-success pull-right" ng-if="log.editing" ng-click="save(row)">Save</button>\
				</td>\
			</tr>\
			</table>\
	<label>Totals:</label> {[total()]}\
	<br><button ng-click="newLog()" class="btn btn-success">New</button>\
	</div></load-on-select>'
	);
}]);
//<table class="table" ng-if="logs.length">\
//<tr class="no-border-top"><th>User</th><th>Category</th><th>Quantity</th><th>Description</th><th>Status</th><th>Exports</th><td></td></tr>\
//<tr ng-repeat="log in logs">\
//<td>{[log.user.first_name]} {[log.user.last_name]}</td>\
//<td ng-if="!log.editing">{[log.category.name]}</span></td>\
//<td ng-if="log.editing">\
//		<p class="error" ng-repeat="error in log.errors.category">{[error]}</p>\
//		<select ng-options="c.id as c.name for c in categories track by c.id" ng-model="log.category" class="form-control"></select>\
//</td>\
//<td ng-if="!log.editing">\
//		{[log.quantity]}\
//</td>\
//<td ng-if="log.editing" style="width:30px">\
//		<p class="error" ng-repeat="error in log.errors.quantity">{[error]}</p>\
//		<input ng-model="log.quantity" size="4" class="form-control"/>\
//</td>\
//<td ng-if="!log.editing">{[log.description]}</td><td ng-if="log.editing"><textarea ng-model="log.description" class="form-control"></textarea></td>\
//<td ng-if="log.editing">\
//	<p class="error" ng-repeat="error in log.errors.status">{[error]}</p>\
//		<select ng-options="key as value for (key,value) in statuses" ng-model="log.status" class="form-control"></select>\
//</td>\
//<td ng-if="!log.editing">{[log.status]}</td>\
//<td><a href="/tracker/exports/#/exports/{[e.id]}/" ng-repeat="e in log.exports" title="{[e.description]}">{[e.created|date]}<span ng-repeat-end ng-if="!$last">, </span></a></td>\
//<td>\
//	<button class="btn btn-xs btn-danger pull-right" ng-click="deleteLog($index)">Delete</button>\
//	<button class="btn btn-xs pull-right" ng-if="!log.editing" ng-click="editLog(log)">Edit</button>\
//	<button class="btn btn-xs btn-success pull-right" ng-if="log.editing" ng-click="save(log)">Save</button>\
//</td>\
//</tr>\
//</table>\

