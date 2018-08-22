
angular.module('mainapp')
.controller('PoolController', ['$scope','DRFNgTableParams','poolService', PoolController]);

function PoolController($scope,DRFNgTableParams,poolService) {
//	$scope.headers=[{'name':'created','label':'Created'},{'name':'name','label':'Name'},{'name':'type','label':'Type'},{'name':'description','label':'Description'}];
	$scope.poolLink = function(pool){return django_js_utils.urls.resolve('pool', { pk: pool.id })};
	$scope.tableParams = DRFNgTableParams('/api/pools/',{sorting: { created: "desc" },default_order:'id'});
	$scope.createPool = function(){
		poolService.create();
	}
}

