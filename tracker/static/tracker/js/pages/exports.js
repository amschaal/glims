
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
                controller: 'ExportController'
            }).
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

app.controller('ExportController', ['$scope','$http', '$routeParams','$location','NgTableParams','DRFNgTableParams','growl', 'Export','Log','SelectModalService', ExportController]);
function ExportController($scope, $http, $routeParams,$location, NgTableParams, DRFNgTableParams, growl,Export,Log,SelectModalService) {
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
		  selectLogsModal({multi:true,initial:$scope.logs}).result.then(
				  function(logs){
//					  $scope.instance.logs = $scope.instance.logs.concat(logs); 
//					  var url = django_js_utils.urls.resolve('add_export_logs',{ pk: $scope.instance.id });
					  var ids = logs.map(function(log){return log.id});
					  Export.add_logs({id:$scope.instance.id},{log_ids:ids},function(response){
						  $scope.logs = $scope.logs.concat(logs);
//						  $scope.tableParams.reload(); 
						  console.log('logs',logs,$scope.logs);
						  $scope.reloadLogs();
				    	},function(response){
				    		growl.error('Unable to add logs',{ttl:3000});
				    	})
					  
//					  $http.post(url,{'log_ids':log_ids})
//						.success(function(){
//							$scope.instance.logs = $scope.instance.logs.concat(logs);
////							$scope.tableParams.reload();
//						})
//						.error(function(){
//							growl.error('Failed to add libraries',{ttl:3000});
//						});
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
	
    $scope.deleteExport = function(){if(!confirm('Are you sure you want to delete this export?'))return;$scope.instance.$remove(function(){$location.path('/');})}
    $scope.saveExport = function(){$scope.instance.$save(function(){growl.success('Saved',{ttl: 3000})})}
    $scope.reloadLogs = function(){
    	$scope.tableParams.settings({
            dataset: $scope.logs
          });
    };
    $scope.loadLogs = function(){
    	$scope.logs = Log.query({exports__id:$routeParams.id,page_size:10000},function(response){
    		console.log('logs',response,$scope.logs);
    		$scope.tableParams = new NgTableParams({}, {
    		      dataset: $scope.logs
    		    });
    	})
    }
//    $scope.tableParams = DRFNgTableParams('/tracker/api/logs/',{filter:{exports__id:$routeParams.id}});
    $scope.containsLog = function(log){
    	var ids = $scope.logs.map(function(log){return log.id});
    	return (ids.indexOf(log.id) >=0)
    }
    $scope.addLog = function(log){
    	if (!$scope.containsLog(log))
    		$scope.logs.push(log);
    	else
    		growl.error("That log is already in the export",{ttl:3000});
    };
    $scope.removeLogs = function(){
    	Export.remove_logs({id:$scope.instance.id},{log_ids:$scope.selection.logs},function(response){
    		_.remove($scope.logs,function(log){return $scope.selection.logs.indexOf(log.id) >-1});
        	$scope.selection.logs = [];
        	$scope.tableParams.reload();
//        	$scope.reloadLogs();
    	},function(response){
    		growl.error('Unable to remove logs',{ttl:3000});
    	})
    };
    $scope.setStatuses = function(status){
    	Log.set_statuses({},{log_ids:$scope.selection.logs,status:status},function(response){
    		_.each(
    				_.filter($scope.logs,function(log){return $scope.selection.logs.indexOf(log.id) >-1}),
    				function(log){log.status = status}
			)
//    		_.remove($scope.instance.logs,function(log){return $scope.selection.logs.indexOf(log.id) >-1});
//        	$scope.selection.logs = [];
    	},function(response){
    		growl.error('Unable to remove logs',{ttl:3000});
    	})
    }
    $scope.getStatuses = function(){
    	return _.map($scope.config.statuses,function(key,val){return {id:key,title:val}});
    };
    $scope.exports = function(){
		$location.path('/');
	}
    $scope.grouped_logs = function(groupBy){
    	return _.groupBy($scope.logs, groupBy);
    }
    $scope.grouped_sums = function(groupBy){
    	return _.mapValues($scope.grouped_logs(groupBy),function(logs){return _.sumBy(logs, 'quantity')});
    }
    $scope.toggle_select = function(val){
    	$scope.selection.logs = val ? $scope.logs.map(function(log){return log.id}) : [];
    		
    }
    $scope.init = function(config){
      console.log('init export',config,$routeParams);
      $scope.selection = {logs:[]};
	  $scope.config = config;
	  if($routeParams.id){
		  $scope.instance = Export.get({id:$routeParams.id},function(foo){console.log(foo)});
		  $scope.loadLogs();
	  }else{
		  var today = new Date();
		  var start_date = new Date();
		  start_date.setMonth(start_date.getMonth()-1);
		  $scope.instance = new Export({start_date:start_date,end_date:today});
	  }
		  
    	  
//	  $scope.options = options;
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
	  $scope.selectAll = function(){
		  console.log('selecting', $scope.tableParams.total());
				var params = $scope.tableParams;
		  		var url_params = params.url();
				var query_params = {page:url_params.page,page_size:10000,ordering:params.orderBy().join(',').replace('+','')};
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
	  $scope.grouped_logs = function(groupBy){
		  return _.groupBy($scope.value, groupBy);
      }
	  $scope.grouped_sums = function(groupBy){
		  return _.mapValues($scope.grouped_logs(groupBy),function(logs){return _.sumBy(logs, 'quantity')});
	  }
	  
	}
)
