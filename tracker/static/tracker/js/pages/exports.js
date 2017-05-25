
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

app.controller('ExportController', ['$scope','$http', '$routeParams','$location','DRFNgTableParams','growl', 'Export','SelectModalService', ExportController]);
function ExportController($scope, $http, $routeParams,$location, DRFNgTableParams, growl,Export,SelectModalService) {
	function selectLogsModal(options){ 
		  var defaultOptions = {
				  title: 'Search logs',
				  controller: 'selectLogsController',
				  tableParams: DRFNgTableParams('/tracker/api/logs/',{sorting: { modified: "desc" },filter: { exclude_export: $routeParams.id }}),
				  template: 'tracker/select_modals/logs_modal.html',
				  return_difference:true
		  }
		  angular.extend(defaultOptions,options?options:{});
		  return SelectModalService.openSelectModal(defaultOptions.template,defaultOptions.tableParams,defaultOptions,{'statuses':$scope.getStatuses()});
	  }
	$scope.selectLogs = function(){
		  selectLogsModal({multi:true,initial:$scope.instance.logs}).result.then(
				  function(logs){
//					  $scope.instance.logs = $scope.instance.logs.concat(logs); 
					  var url = django_js_utils.urls.resolve('add_export_logs',{ pk: $scope.instance.id });
					  var log_ids = logs.map(function(log){return log.id});
					  $http.post(url,{'log_ids':log_ids})
						.success(function(){
							$scope.instance.logs = $scope.instance.logs.concat(logs);
//							$scope.tableParams.reload();
						})
						.error(function(){
							growl.error('Failed to add libraries',{ttl:3000});
						});
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
    $scope.grouped_logs = function(){
    	return _.groupBy($scope.instance.logs, 'status');
    }
    $scope.grouped_sums = function(){
    	return _.mapValues($scope.grouped_logs(),function(logs){return _.sumBy(logs, 'quantity')});
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

app.controller('selectLogsController', function ($scope,$http, $uibModalInstance,initial,tableParams,template,options,context) {
	  $scope.context = context;
	  if (options.return_difference){
		  $scope.previously_selected = angular.copy(initial);
		  $scope.value = [];
	  }
	  else
		  $scope.value = angular.copy(initial);
	  $scope.tableParams = tableParams;
	  $scope.template = template;
	  $scope.options = options;
	  $scope.select = function(row){
		  $uibModalInstance.close(row);
	  }
	  $scope.addAll = function(){
		  console.log('adding', $scope.tableParams.total());
				var params = $scope.tableParams;
		  		var url_params = params.url();
				var query_params = {page:url_params.page,page_size:url_params.count,ordering:params.orderBy().join(',').replace('+','')};
				angular.extend(query_params, params.filter());
				// ajax request to api
				return $http.get('/tracker/api/logs/',{params:query_params}).then(function(response){
					params.total(response.data.count);
					console.log(response.data.results);
					$scope.value = _.differenceBy(_.unionBy(response.data.results,$scope.value,'id'),$scope.previously_selected,'id');
/*					if (resource)
						return response.data.results.map(function(obj){return new resource(obj);});
					else
						return response.data.results;
						*/
				});
	  }
	  $scope.removeAll = function(){ $scope.value=[];}
	  $scope.save = function(){
		  $uibModalInstance.close($scope.value);
	  }
	  $scope.cancel = function(){
		  $uibModalInstance.dismiss();
	  }
	  $scope.add = function(row){
		  if(!angular.isArray($scope.value))
			  $scope.value = [row];
		  else
			  $scope.value.push(row);
	  }
	  $scope.remove = function(row){
		  if(!angular.isArray($scope.value))
			  $scope.value=null;
		  else{
			  for(var i in $scope.value){
				  if ($scope.value[i][options.id] == row[options.id]){
					  $scope.value.splice(i,1);
					  return;
				  }
			  }
		  }
	  }
	  $scope.isAllowed = function(row){
		  if(!angular.isArray($scope.previously_selected))
			  return true;
		  var filter = {};
		  filter[options.id] = row[options.id];
		  return !_.find($scope.previously_selected, filter);
	  }
	  $scope.isSelected = function(row){
		  if(!angular.isArray($scope.value))
			  return false;
		  var filter = {};
		  filter[options.id] = row[options.id];
		  return _.find($scope.value, filter);
	  }
	  
	}
)
