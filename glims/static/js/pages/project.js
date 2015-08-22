
angular.module('mainapp')
.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            
            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}])
.controller('SamplesController', ['$scope','$http','Sample', SamplesController]);

function SamplesController($scope,$http,$Sample) {
	var sampleDefaults;
	$scope.errors = false;
	$scope.setSampleDefaults = function(defaults){
		sampleDefaults = defaults;
		
	};
	$scope.save = function(sample){
		console.log('save',sample);
		var onSuccess = function(response){delete sample.errors;};
		var onError = function(response){sample.errors = response.data;console.log(response.data);};
		if(sample.id)
			sample.$save(onSuccess,onError);
		else
			sample.$create(onSuccess,onError);
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
	$scope.uploadFile = function(url){
        var file = $scope.myFile;
        console.log('file is ' );
        console.dir(file);
        
        var fd = new FormData();
        fd.append('tsv', file);

        $http.post(url, fd, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        })
        .success(function(data){
        	$scope.errors = false;
        	for (var i in data){
        	var sample = new $Sample(data[i]);
	    		sample.editing=true;
	    		$scope.samples.push(sample);	
        	}
        })
        .error(function(data){
        	console.log('errors',data)
        	$scope.errors = data.errors;
        });
        
    };
	$scope.init = function(){
		$scope.samples = $Sample.query(sampleDefaults,function() {
			angular.forEach($scope.samples,function(sample){
				//$scope.addNote(note);
			});
		});
	}
	
	
	
}

