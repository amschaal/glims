
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

app.controller('ExportController', ['$scope', '$routeParams','$location','DRFNgTableParams','growl', 'Export','SelectModalService', ExportController]);
function ExportController($scope, $routeParams,$location, DRFNgTableParams, growl,Export,SelectModalService) {
	function selectLogsModal(options){ 
		  var defaultOptions = {
				  title: 'Search logs',
				  tableParams: DRFNgTableParams('/tracker/api/logs/',{sorting: { modified: "desc" }}),
				  template: 'tracker/select_modals/logs_modal.html',
				  return_difference:true
		  }
		  angular.extend(defaultOptions,options?options:{});
		  return SelectModalService.openSelectModal(defaultOptions.template,defaultOptions.tableParams,defaultOptions);
	  }
	$scope.selectLogs = function(){
		  selectLogsModal({multi:true,initial:$scope.instance.logs}).result.then(
				  function(logs){
					  $scope.instance.logs = $scope.instance.logs.concat(logs); 
					  
//					  var url = django_js_utils.urls.resolve('add_pool_libraries',{ pk: pool_id });
//					  var library_ids = libraries.map(function(library){return library.id});
//					  $http.post(url,{'library_ids':library_ids})
//						.success(function(){
//							$scope.libraries = libraries;	
//							$scope.tableParams.reload();
//						})
//						.error(function(){
//							alert('Failed to add libraries');
//						});
				  });
	  }
	console.log('export controller')
	$scope.selection = {logs:[]};
	$scope.instance = Export.get({id:$routeParams.id},function(foo){console.log(foo)});
    $scope.deleteExport = function(){$scope.instance.$remove(function(){$location.path('/');})}
    $scope.saveExport = function(){$scope.instance.$save(function(){growl.success('Saved',{ttl: 3000})})}
    $scope.tableParams = DRFNgTableParams('/tracker/api/logs/',{});
    $scope.containsLog = function(log){
    	var ids = $scope.instance.logs.map(function(log){return log.id});
    	return (ids.indexOf(log.id) >=0)
    }
    $scope.addLog = function(log){
    	if (!$scope.containsLog(log))
    		$scope.instance.logs.push(log);
    	else
    		growl.error("That log is already in the export",{ttl:3000});
    };
    $scope.removeLogs = function(){
    	_.pullAllBy($scope.instance.logs,$scope.selection.logs,'id');
    	$scope.selection.logs = [];
    };
    $scope.getStatuses = function(){
    	return _.map($scope.statuses,function(key,val){return {id:key,title:val}});
    };
    $scope.exports = function(){
		$location.path('/');
	}
};

app.controller('ExportsController', ['$scope','$location','DRFNgTableParams','growl','Export','Log', ExportsController]);
function ExportsController($scope,$location,DRFNgTableParams,growl,Export,Log) {
	$scope.tableParams = DRFNgTableParams('/tracker/api/exports/',{});
	$scope.createExport = function(){
		var log_export = new Export({logs:[]});
		log_export.$create(function(){console.log('log_export',log_export);$location.path('/exports/'+log_export.id+'/');});
	};
	$scope.edit = function(id){
		$location.path('/exports/'+id+'/');
	}
}
