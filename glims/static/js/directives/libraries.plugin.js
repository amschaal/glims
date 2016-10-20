
angular.module("libraries-plugin", ['glims.formly','glimsModels']);

angular.module('plugins').requires.push("libraries-plugin")

angular.module("libraries-plugin")
.directive('sampleLibraries', function(Sample,Library,Barcode,sampleService) {
	return {
		restrict: 'AE',
		templateUrl: 'template/plugins/sample_libraries.html',
		scope: {
			sample:'=',
			getURL:'&'
		},
		controller: function ($scope,$rootScope,$http,$log,$uibModal) {
			$scope.getURL = $rootScope.getURL;
			$scope.errors = false;
			$scope.barcodes = Barcode.query();
			function updateLibraryCount(){
				$rootScope.library_count = $scope.libraries ? $scope.libraries.length : 0;
			}
			$scope.refreshLibraries = function(){
				console.log('refreshing libraries',$scope.sample);
				$scope.libraries = Library.query({sample:$scope.sample.id},function() {
					updateLibraryCount()
				});
			}
			$scope.$watch('sample.id',function(newValue,oldValue){
				if (newValue)
					$scope.refreshLibraries();
			});
		}

	}
});


angular.module("libraries-plugin").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/plugins/sample_libraries.html',
			'<load-on-select>\
			<h3>Libraries</h3>\
			{[libraries]}\
			{[barcodes]}\
			</load-on-select>'
	);
}]);

