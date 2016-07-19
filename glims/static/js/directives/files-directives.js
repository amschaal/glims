angular.module('files.directives', ["ngTable"])
.directive('listFiles', function() {
	  return {
	    restrict: 'AE',
	    templateUrl: 'template/files/list.html',
	    scope: {
	    	baseUrl:'@',
	    	subdir: '@'
	    },
	    controller: function($scope, $http, $element,NgTableParams){
	    	var listUrl = $scope.baseUrl + 'list_files/';
	    	var downloadUrl = $scope.baseUrl + 'download/';
	    	$scope.tableParams = new NgTableParams();
	    	$scope.directories = $scope.subdir ? $scope.subdir.split('/') : [];
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
	<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed">\
      <tr ng-repeat="row in $data track by row.name">\
	      <td data-title="\'Name\'" sortable="\'name\'" filter="{name: \'text\'}"><a ng-if="row.is_dir" ng-click="getFiles(row.name)"><i class="glyphicon glyphicon-folder-open"> </i> {[row.name]}</a><a href="{[download(row.name)]}" ng-if="!row.is_dir">{[row.name]}</a></td>\
		  <td data-title="\'Extension\'" sortable="\'extension\'" filter="{extension: \'text\'}">{[row.extension]}</td>\
		  <td data-title="\'Size\'" sortable="\'bytes\'">{[row.bytes|bytes]}</td>\
	   </tr>\
	 </table>'
	  );
	}]);

