angular.module("logger-plugin");

angular.module('plugins').requires.push("logger-plugin");

angular.module("logger-plugin")
.directive('objectLogs', function(Account) {
	return {
		restrict: 'AE',
		templateUrl: 'template/logger/logs.html',
		scope: {
			objectId:'=',
			contentType:'='
		},
		controller: function ($scope,$rootScope,DRFNgTableParams,Log) {
			$scope.tableParams = DRFNgTableParams('/logger/api/logs/',{sorting: { created: "desc" },filter:{content_type:$scope.contentType,object_id:$scope.objectId}},Log);
		}
	}
});

angular.module("logger-plugin").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/logger/logs.html',
	'<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed">\
		<tr ng-repeat="row in $data track by row.id">\
			<td data-title="\'Created\'" sortable="\'created\'">{[row.created|date:\'short\']}</td>\
			<td data-title="\'Text\'" filter="{text__icontains: \'text\'}"><a href="{[row.url]}" ng-if="row.url">{[row.text]}</a><span ng-if="!row.url">{[row.text]}</span></td>\
			<td data-title="\'Description\'" filter="{description__icontains: \'text\'}">{[row.description]}</td>\
		</tr>\
    </table>');
}]);


