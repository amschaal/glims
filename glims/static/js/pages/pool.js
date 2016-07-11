
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
.controller('SamplesController', ['$scope','Sample','Pool','$http','DRFNgTableParams','selectModalService', SamplesController]);

function SamplesController($scope,$Sample,$Pool,$http,DRFNgTableParams,selectModalService) {
//	var sampleURL = django_js_utils.urls.resolve('sample-list');
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	var pool_id = null;
	$scope.sample_data={};
	function refreshSamples(){
		$scope.samples = $Sample.query({pool:pool_id});
	}
	$scope.removeSample = function (sample,index){
		var url = django_js_utils.urls.resolve('remove_pool_samples',{ pk: pool_id });
		$http.post(url,{'sample_ids':[sample.id]})
		.success(function(){
			for (var i in $scope.samples){
				if ($scope.samples[i].id == sample.id)
					$scope.samples.splice(i,1);
				delete $scope.sample_data[String(sample.id)];
			}
			
		})
		.error(function(){
			alert('Failed to delete sample');
		});
		
	}
	$scope.init = function(data){
		pool_id = data.pool_id;
		$Pool.get({id:pool_id},function(data){
			$scope.sample_data = data.sample_data;
		});
		refreshSamples();
//		$http.get(sampleURL,{})
//		.success(function(data){
//			
//		})
	};
	$scope.overriddenFields = function(sample){
		var data = $scope.sample_data[String(sample.id)] ? $scope.sample_data[String(sample.id)] : {};
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
	$scope.open = function (sample,size) {

	    var modalInstance = $modal.open({
	      templateUrl: 'myModalContent.html',
	      controller: 'ModalInstanceCtrl',
	      size: size,
	      resolve: {
	    	  sample: function () {
		          return sample;
		      },
		      pool_id: function () {
		          return pool_id;
		      },
		      sample_data: function(){
		        	return $scope.sample_data[String(sample.id)] ? $scope.sample_data[String(sample.id)] : {};
		      }
//	        items: function () {
//	          return $scope.items;
//	        }
	      }
	    });

	    modalInstance.result.then(function (data) {
	      $scope.sample_data[String(data.sample.id)] = data.data;
	    }, function () {
//	      $log.info('Modal dismissed at: ' + new Date());
	    });
	  };
	  $scope.sampleTableParams = DRFNgTableParams('/api/samples/',{sorting: { created: "desc" }});
	  $scope.selectSamples = selectModalService.selectSamples;
	
}


// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $modal service used above.

angular.module('mainapp').controller('ModalInstanceCtrl', function ($scope, $http, $modalInstance, sample, pool_id, sample_data) {
	$scope.sample = sample;
	var pool_id = pool_id;
	$scope.override = {}
	$scope.errors={};
	$scope.sample_data = sample_data;
	angular.forEach(Object.keys(sample_data),function(key,val){
		$scope.override[key]=true;
	});
	$scope.override['data']={};
	if (sample_data.data){
		angular.forEach(Object.keys(sample_data.data),function(key,val){
			$scope.override['data'][key]=true;
		});
	}
	var get_overridden_data = function(){
		var data = {};
		angular.forEach(Object.keys($scope.override),function(key,value){
			console.log(key,value);
			if($scope.override[key])
				data[key]=$scope.sample_data[key];
		});
		data['data']={};
		angular.forEach(Object.keys($scope.override['data']),function(key,value){
			if($scope.override['data'][key])
				data['data'][key]=$scope.sample_data['data'][key];
		});
		return data;
	};
	
	$scope.getErrors = function(name){
		return $scope.errors[name] ? $scope.errors[name] : []; 
	};
	$scope.ok = function () {
		var url = django_js_utils.urls.resolve('update_pool_sample', { pool_id: pool_id, sample_id: $scope.sample.id});
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
				$modalInstance.close({'sample':$scope.sample,'data':data.data});
			}
			
		});
		
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
