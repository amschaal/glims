
angular.module('mainapp')
.controller('SamplesController', ['$scope','Sample', SamplesController]);

function SamplesController($scope,$Sample) {
	var sampleDefaults;
	$scope.setSampleDefaults = function(defaults){
		sampleDefaults = defaults;
		
	};
	$scope.save = function(sample){
		console.log('save',sample);
		if(sample.id)
			sample.$save();
		else
			sample.$create();
	};
	$scope.addSample = function(){
		var sample = new $Sample(sampleDefaults);
		sample.editing=true;
		$scope.samples.push(sample);
		console.log('sample',sample);
	};
	$scope.cancel = function(sample,index){
		sample.editing=false;
		if(!sample.id)
			$scope.samples.splice(index,1);
	};
	$scope.deleteSample = function(sample,index){
		if (!confirm("Are you sure you want to delete this sample and all associated data?"))
			return;
		sample.$remove(function(){$scope.samples.splice(index,1);});
	};
	$scope.sampleLink = function(sample){return django_js_utils.urls.resolve('sample', { pk: sample.id })};
	$scope.init = function(){
		$scope.samples = $Sample.query(sampleDefaults,function() {
			angular.forEach($scope.samples,function(sample){
				//$scope.addNote(note);
			});
		});
	}
	
	
	
}

