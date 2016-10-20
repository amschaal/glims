
angular.module('mainapp').requires.push('glims.formly','selectModals');
angular.module('mainapp').controller('PoolController', ['$scope','$http','Pool','growl','poolService', PoolController]);

function PoolController($scope,$http,$Pool,growl,poolService) {
//	$scope.errors={};
//	$scope.message = false;
	var pool_id = null;
	$scope.init = function(params){
		pool_id = params.pool_id;
		$scope.pool = $Pool.get({'id':pool_id});
	}
//	$scope.onError = function(data,status,headers,config){
//		growl.error('There were errors updating the pool',{ttl: 4000});
//	}
//	$scope.onSuccess = function(data,status,headers,config){
//		growl.success('Pool updated',{ttl: 4000});
//	}
	$scope.updatePool = function(){
		poolService.update($scope.pool)
			.result.then(
	    			function (pool) {
	    		    	$scope.pool = pool;
	    		    }
	    	);
	}
}
angular.module('mainapp')
.controller('LibrariesController', ['$scope','Library','Pool','$http','DRFNgTableParams','SelectModalService', LibrariesController]);

function LibrariesController($scope,$Library,$Pool,$http,DRFNgTableParams,SelectModalService) {
	
	console.log('SelectModalService', SelectModalService)
//	var sampleURL = django_js_utils.urls.resolve('sample-list');
	$scope.sampleLink = function(library){return django_js_utils.urls.resolve('sample', { pk: library.sample.id })};
	var pool_id = null;
	$scope.library_data={};
	function refreshLibraries(){
		$scope.libraries = $Library.query({pool:pool_id});
	}
	$scope.removeLibrary = function (library,index){
		var url = django_js_utils.urls.resolve('remove_pool_libraries',{ pk: pool_id });
		$http.post(url,{'library_ids':[library.id]})
		.success(function(){
			for (var i in $scope.libraries){
				if ($scope.libraries[i].id == library.id)
					$scope.libraries.splice(i,1);
				delete $scope.library_data[String(library.id)];
			}
			
		})
		.error(function(){
			alert('Failed to delete library');
		});
		
	}
	$scope.init = function(data){
		pool_id = data.pool_id;
		$Pool.get({id:pool_id},function(data){
			$scope.library_data = data.library_data;
		});
		refreshLibraries();
//		$http.get(sampleURL,{})
//		.success(function(data){
//			
//		})
	};
	$scope.overriddenFields = function(library){
		var data = $scope.library_data[String(library.id)] ? $scope.library_data[String(library.id)] : {};
		var fields = [];
		angular.forEach(Object.keys(data),function(key,val){
			if (key != 'data')
				fields.push(key);
		});
		if (data.data){
			angular.forEach(Object.keys(data.data),function(key,val){
				fields.push(key);
			});
		}
		return fields.join(', ');
	}
	$scope.open = function (library,size) {

	    var modalInstance = $modal.open({
	      templateUrl: 'myModalContent.html',
	      controller: 'ModalInstanceCtrl',
	      size: size,
	      resolve: {
	    	  library: function () {
		          return library;
		      },
		      pool_id: function () {
		          return pool_id;
		      },
		      library_data: function(){
		        	return $scope.library_data[String(library.id)] ? $scope.library_data[String(library.id)] : {};
		      }
//	        items: function () {
//	          return $scope.items;
//	        }
	      }
	    });

	    modalInstance.result.then(function (data) {
	      $scope.library_data[String(data.sample.id)] = data.data;
	    }, function () {
//	      $log.info('Modal dismissed at: ' + new Date());
	    });
	  };
	  $scope.selectLibraries = function(){
		  SelectModalService.selectLibraries({multi:true,initial:$scope.libraries}).result.then(
				  function(libraries){
					  var url = django_js_utils.urls.resolve('add_pool_libraries',{ pk: pool_id });
					  var library_ids = libraries.map(function(library){return library.id});
					  $http.post(url,{'library_ids':library_ids})
						.success(function(){
							$scope.libraries = libraries;							
						})
						.error(function(){
							alert('Failed to add libraries');
						});
				  });
	  }
	
}


// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $modal service used above.

angular.module('mainapp').controller('ModalInstanceCtrl', function ($scope, $http, $modalInstance, library, pool_id, library_data) {
	$scope.library = library;
	var pool_id = pool_id;
	$scope.override = {}
	$scope.errors={};
	$scope.library_data = library_data;
	angular.forEach(Object.keys(library_data),function(key,val){
		$scope.override[key]=true;
	});
	$scope.override['data']={};
	if (library_data.data){
		angular.forEach(Object.keys(library_data.data),function(key,val){
			$scope.override['data'][key]=true;
		});
	}
	var get_overridden_data = function(){
		var data = {};
		angular.forEach(Object.keys($scope.override),function(key,value){
			console.log(key,value);
			if($scope.override[key])
				data[key]=$scope.library_data[key];
		});
		data['data']={};
		angular.forEach(Object.keys($scope.override['data']),function(key,value){
			if($scope.override['data'][key])
				data['data'][key]=$scope.library_data['data'][key];
		});
		return data;
	};
	
	$scope.getErrors = function(name){
		return $scope.errors[name] ? $scope.errors[name] : []; 
	};
	$scope.ok = function () {
		var url = django_js_utils.urls.resolve('update_pool_library', { pool_id: pool_id, library_id: $scope.library.id});
		var data = get_overridden_data();
		console.log('data',data);
		$http.post(
			url,
			data
		).success(function(data, status, headers, config) {
			if (data.errors){
				$scope.errors=data.errors;
			}
			else{
				$modalInstance.close({'library':$scope.library,'data':data.data});
			}
			
		});
		
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
