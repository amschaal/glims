
angular.module('mainapp')
.controller('SampleFormController', ['$scope','$http', SampleFormController]);

function SampleFormController($scope,$http) {
	$scope.choice = {};
//	$scope.project = {};
	$scope.choices = [];
	$scope.refreshChoices= function(search) {
	    var params = {search: search};
	    if (search.length < 2)
	    	return [];
	    return $http.get('/api/projects/', {params: params})
	      .then(function(response) {
	        $scope.choices = response.data.results;
	      });
	};
	$scope.selectChoice = function ($item,$model){
		//set hidden input here!
		console.log($item,$model);
	}
}

