
angular.module('mainapp')
.controller('SampleFormController', ['$scope','$http', SampleFormController]);

function SampleFormController($scope,$http) {
	$scope.project = 'blah';
	$scope.projects = [];
	$scope.refreshProjects= function(search) {
	    var params = {search: search};
	    return $http.get('/api/projects/', {params: params})
	      .then(function(response) {
	        $scope.projects = response.data.results;
	      });
	};
}

