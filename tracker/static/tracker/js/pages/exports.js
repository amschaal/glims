
var app = angular.module('mainapp');
app.requires.push('ngRoute');



app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/', {
                templateUrl: 'exports.html',
                controller: 'ExportsController'
            }).
//            when('/exports/new/', {
//                templateUrl: 'export.html',
//                controller: 'RouteController'
//            }).
            when('/exports/:id/', {
                templateUrl: 'export.html',
                controller: 'ExportController'
            }).
            otherwise({
                redirectTo: '/exports/'
            });
    }]);

app.controller("RouteController", function($scope, $routeParams) {
    $scope.param = $routeParams.param;
});

app.controller('ExportController', ['$scope', '$routeParams','$location','DRFNgTableParams','growl', 'Export', ExportController]);
function ExportController($scope, $routeParams,$location, DRFNgTableParams, growl,Export) {
	console.log('export controller')
	$scope.instance = Export.get({id:$routeParams.id},function(foo){console.log(foo)});
    $scope.deleteExport = function(){$scope.instance.$remove(function(){$location.path('/');})}
    $scope.saveExport = function(){$scope.instance.$save(function(){growl.success('Saved',{ttl: 3000})})}
    $scope.tableParams = DRFNgTableParams('/tracker/api/logs/',{});
    $scope.addLog = function(log){
    	$scope.instance.logs.push(log);
    };
    $scope.removeLog = function(log){
    	$scope.instance.logs.splice($scope.instance.logs.indexOf(log),1);
    };
};

app.controller('ExportsController', ['$scope','$location','DRFNgTableParams','growl','Export','Log', ExportsController]);
function ExportsController($scope,$location,DRFNgTableParams,growl,Export,Log) {
	$scope.tableParams = DRFNgTableParams('/tracker/api/exports/',{});
	$scope.createExport = function(){
		var log_export = new Export({});
		log_export.$create(function(){console.log('log_export',log_export);$location.path('/exports/'+log_export.id+'/');});
	};
	$scope.edit = function(id){
		$location.path('/exports/'+id+'/');
	}
}
