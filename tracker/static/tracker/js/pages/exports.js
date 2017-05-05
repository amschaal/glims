
var app = angular.module('mainapp');
app.requires.push('ngRoute');



app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/', {
                templateUrl: 'exports.html',
                controller: 'ExportsController'
            }).
            when('/exports/new/', {
                templateUrl: 'export.html',
                controller: 'RouteController'
            }).
            when('/exports/:id/', {
                templateUrl: 'export.html',
                controller: 'RouteController'
            }).
            otherwise({
                redirectTo: '/exports/'
            });
    }]);

app.controller("RouteController", function($scope, $routeParams) {
    $scope.param = $routeParams.param;
})

app.controller('ExportsController', ['$scope','$location','DRFNgTableParams','growl','Export','Log', ExportsController]);
function ExportsController($scope,$location,DRFNgTableParams,growl,Export,Log) {
	$scope.tableParams = DRFNgTableParams('/tracker/api/exports/',$scope.tableSettings);
	$scope.createExport = function(){
		var log_export = new Export({});
		log_export.$create(function(){console.log('log_export',log_export)});
		$location.path('/exports/4/');
	};
}