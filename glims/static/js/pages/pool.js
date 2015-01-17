
angular.module('mainapp')
.controller('PoolController', ['$scope','$http', PoolController]);

function PoolController($scope,$http) {
	$scope.print = function(){console.log('pool',$scope.pool)};
	$scope.errors={};
	$scope.message = false;
	$scope.getErrors = function(name){
		return $scope.errors[name] ? $scope.errors[name] : []; 
	};
	$scope.submit = function(){
		var url = django_js_utils.urls.resolve('update_pool', { pk: 6});
		$http.post(
			url,
			$scope.pool
		).success(function(data, status, headers, config) {
			console.log('data',data);
			if (data.errors){
				$scope.errors=data.errors;
				$scope.message = false;
			}
			else{
				$scope.errors = {}
				$scope.message = "Saved successfully.";
			}
				
		});
	}
	
}


angular.module('mainapp')
.controller('SamplesController', ['$scope','Sample','$http','$modal', SamplesController]);

function SamplesController($scope,$Sample,$http,$modal) {
//	var sampleURL = django_js_utils.urls.resolve('sample-list');
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	function refreshSamples(){
		$scope.samples = $Sample.query({pool:$scope.pool});
	}
	$scope.removeSample = function (sample,index){
		var url = django_js_utils.urls.resolve('remove_pool_samples',{ pk: $scope.pool });
		$http.post(url,{'sample_ids':[sample.id]})
		.success(function(){
			for (var i in $scope.samples){
				if ($scope.samples[i].id == sample.id)
					$scope.samples.splice(i,1);
			}
		})
		.error(function(){
			alert('Failed to delete sample');
		});
		
	}
	$scope.init = function(data){
		$scope.pool = data.pool;
		console.log('samples');
		refreshSamples();
//		$http.get(sampleURL,{})
//		.success(function(data){
//			
//		})
	};
	
	$scope.open = function (sample,size) {

	    var modalInstance = $modal.open({
	      templateUrl: 'myModalContent.html',
	      controller: 'ModalInstanceCtrl',
	      size: size,
	      resolve: {
	    	  sample: function () {
		          return sample;
		        },
		        sample_data: function(){return {'description':'blah','name':'foo'};}
//	        items: function () {
//	          return $scope.items;
//	        }
	      }
	    });

	    modalInstance.result.then(function (selectedItem) {
	      $scope.selected = selectedItem;
	    }, function () {
	      $log.info('Modal dismissed at: ' + new Date());
	    });
	  };
	
	
}


// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $modal service used above.

angular.module('mainapp').controller('ModalInstanceCtrl', function ($scope, $modalInstance, sample, sample_data) {
	console.log('sample',sample);
	console.log('sample_data',sample_data)
	$scope.sample = sample;
	$scope.override = {}
	angular.forEach(Object.keys(sample_data),function(key,val){
		$scope.override[key]=true;
	})
		
	$scope.sample_data = sample_data;
	
	$scope.ok = function () {
    $modalInstance.close($scope.selected);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
