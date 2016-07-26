angular.module('files.directives', ["ngTable"])
.directive('listFiles', function() {
	  return {
	    restrict: 'AE',
	    templateUrl: 'template/files/list.html',
	    scope: {
	    	baseUrl:'@',
	    	subdir: '@',
	    	selection: '=',
	    	actions: '='
	    },
	    controller: function($scope, $http, $element,NgTableParams){
	    	var listUrl = $scope.baseUrl + 'list_files/';
	    	var downloadUrl = $scope.baseUrl + 'download/';
	    	
	    	$scope.tableParams = new NgTableParams();
	    	$scope.directories = $scope.subdir ? $scope.subdir.split('/') : [];
	    	if ($scope.selection)
	    		$scope.selection = angular.isArray($scope.selection) ? $scope.selection : [];
	    	$scope.getFiles = function(directory){
	    		var subdir = $scope.directories;
	    		if (directory){
	    			if(angular.isArray(directory))
	    				subdir = directory;
	    			else
	    				subdir.push(directory);
	    		}
	    		$http.get(listUrl,{params:{subdir:subdir.join('/')}}).then(function(response){
	    			$scope.basedir = response.data.basedir;
    				$scope.directories = subdir;
	    			$scope.files=response.data.files;
	    			$scope.tableParams.settings({dataset:$scope.files});
	    		});
	    	};
	    	$scope.goToDirectoryIndex = function(index){
	    		$scope.getFiles($scope.directories.splice(0,index+1));
	    	};
	    	$scope.download = function(file){
	    		var pathArray = $scope.directories.concat(file)
	    		return downloadUrl + '?subpath=' + pathArray.join('/');
	    	};
	    	$scope.getPath = function(name){
	    		return $scope.directories.concat(name).join('/');
	    	}
	    	$scope.selected = function(name){
	    		return $scope.selection.indexOf($scope.getPath(name)) != -1;
	    	}
	    	$scope.select = function(name){
	    		if (!$scope.selected(name))
	    			$scope.selection.push($scope.getPath(name));
	    	}
	    	$scope.deselect = function(path){
	    		var index = $scope.selection.indexOf(path);
	    		if (!index != -1)
	    			$scope.selection.splice(index,1);
	    	};
	    	$scope.getFiles();
	    	
	    }
	  }
	})
	.filter('bytes', function() {
	return function(bytes, precision) {
		if (bytes==0 || isNaN(parseFloat(bytes)) || !isFinite(bytes)) return '-';
		if (typeof precision === 'undefined') precision = 1;
		var units = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'],
			number = Math.floor(Math.log(bytes) / Math.log(1024));
		return (bytes / Math.pow(1024, Math.floor(number))).toFixed(precision) +  ' ' + units[number];
	}
	})
	.run(['$templateCache', function($templateCache) {
	  $templateCache.put('template/files/list.html',
	'<a ng-click="getFiles([])" ng-if="directories.length > 0">{[basedir]}</a><span ng-if="directories.length < 1">{[basedir]}</span>/<span ng-repeat="dir in directories"><a ng-click="goToDirectoryIndex($index)" ng-if="!$last">{[dir]}</a><span ng-if="$last">{[dir]}</span>/</span>\
	<div ng-if="selection.length > 0" title="{[selection.join(\', \')]}">{[selection.length]} selected</div>\
	<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed">\
      <tr ng-repeat="row in $data track by row.name">\
	      <td data-title="\'Name\'" sortable="\'name\'" filter="{name: \'text\'}"><a ng-if="row.is_dir" ng-click="getFiles(row.name)"><i class="glyphicon glyphicon-folder-open"> </i> {[row.name]}</a><a href="{[download(row.name)]}" ng-if="!row.is_dir"><i class="glyphicon glyphicon-download"> </i> {[row.name]}</a></td>\
		  <td data-title="\'Extension\'" sortable="\'extension\'" filter="{extension: \'text\'}">{[row.extension]}</td>\
		  <td data-title="\'Size\'" sortable="\'bytes\'">{[row.bytes|bytes]}</td>\
		  <td data-title="\'Modified\'" sortable="\'modified\'">{[row.modified]}</td>\
		  <td data-title="\'Actions\'" ng-if="actions"><button ng-if="!selected(row.name) && actions.select" ng-click="select(row.name)" class="btn">Select</button><button ng-click="deselect(getPath(row.name))" ng-if="selected(row.name) && actions.deselect" class="btn btn-danger">Deselect</button></td>\
	   </tr>\
	 </table>'
	  );
	}]);

