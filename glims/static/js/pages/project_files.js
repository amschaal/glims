
angular.module('mainapp')
.controller('ProjectFilesController', ['$scope','$http', ProjectFilesController]);

function ProjectFilesController($scope,$http) {
	$scope.pathArray = [];
	$scope.init = function(base_url){
		$scope.base_url = base_url;
		$scope.listDir('');
	};
	$scope.listDir = function(path){
		if (path != '')
			$scope.pathArray.push(path);
		$scope.getFiles();
	};
	$scope.goUp = function(){
		$scope.pathArray.pop();
		$scope.getFiles();
	};
	$scope.getFiles = function(){
		var url = $scope.base_url + $scope.pathArray.join('/');
		$http.get(url).success(
			function(data){
				$scope.data = data;
	//			$scope.query_params.path = path;
	//			console.log($scope.query_params)
			}
		)
	}
//	$scope.samplesLink = function(lab){return django_js_utils.urls.resolve('samples')+"?project__lab__name="+lab.name;};
}

