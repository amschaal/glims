
var app = angular.module('mainapp');
app.requires.push('glims.formly');
app.controller('SampleController', ['$scope','$log','sampleService', 'ModelType', 'Sample',SampleController])
function SampleController($scope , $log, sampleService, ModelType, Sample){
	$scope.init = function (params){
		$scope.sample = Sample.get({id:params.sample});
	};
	$scope.editSample = function(){
		sampleService.update($scope.sample)
		.result.then(
				function (sample) {
					$scope.sample = sample;
				}
				);
	}
}
