
/**
 * Master Controller
 */


angular.module('Dashboard')
.controller('AjaxController', ['$scope', '$http', AjaxController]);

function AjaxController($scope,  $http) {
	$scope.rows=[];
	var url = '/api/experiments';
	$scope.params={}
	$scope.settings = {'page_size':2,'page':1};
	$scope.headers=[{'name':'name','label':'Name'},{'name':'description','label':'Description'}];
	$scope.parameter_map={'order_by':'ordering','page':'page','page_size':'page_size'};
	$scope.load = function () {
//  	  $scope.urlApi = '/api/experiments/?' + params;
	  for (k in $scope.parameter_map){
		  if ($scope.settings[k])
			  $scope.params[$scope.parameter_map[k]]=$scope.settings[k];
	  }
  	  $http.get(url,{'params':$scope.params}).then(
  			  function (response) {
  				  $scope.count = response.data.count;
  				  if ($scope.settings.page_size){
  					  $scope.settings.pages = Math.ceil($scope.count / $scope.settings.page_size)
  				  }
  				  $scope.rows = response.data.results;
  			  }
  	  );
  	};
  	$scope.Range = function(start, end) {
  	    var result = [];
  	    for (var i = start; i <= end; i++) {
  	        result.push(i);
  	    }
  	    return result;
  	};
  	$scope.orderBy = function(header){
  		if ($scope.settings.order_by == header.name)
  			$scope.settings.order_by = '-' + header.name;
  		else
  			$scope.settings.order_by = header.name;
  		$scope.load();
  	};
  	$scope.setPageSize = function(size){
  		$scope.settings.page_size=size;
  		$scope.goToPage(1);
  	};
  	$scope.goToPage = function (page){
  		$scope.settings.page = page;
  		$scope.settings.page = page;
  		$scope.load();
  	};
  	$scope.next = function(){
  		if ($scope.settings.page < $scope.settings.pages){
  			$scope.goToPage($scope.settings.page + 1)
  		}
  	}
  	$scope.prev = function(){
  		if ($scope.settings.page > 1){
  			$scope.goToPage($scope.settings.page - 1)
  		}
  	}
}

