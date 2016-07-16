angular.module('files.directives', ["ngTable"])
.directive('listFiles', function() {
	  return {
	    restrict: 'AE',
	    templateUrl: 'template/files/list.html',
	    scope: {
	    	listUrl:'@',
	    	subdir: '@'
	    },
	    controller: function($scope, $http, $element,NgTableParams){
	    	$scope.tableParams = new NgTableParams();
	    	$scope.subdir = $scope.subdir ? $scope.subdir : ''
	    	$scope.getFiles = function(subdir){
	    		var new_dir = $scope.subdir;
	    		if (subdir)
	    			new_dir +=  subdir + '/';
	    			console.log('new_dir',new_dir);
	    		$http.get($scope.listUrl,{params:{subdir:new_dir}}).then(function(response){
    				$scope.subdir = new_dir;
	    			$scope.files=response.data;
	    			$scope.tableParams.settings({dataset:$scope.files});
	    		});
	    	};
	    	$scope.getFiles();
	    	
	    }
	  }
	}).run(['$templateCache', function($templateCache) {
	  $templateCache.put('template/files/list.html',
	'{[subdir]}<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed">\
      <tr ng-repeat="row in $data track by row.name">\
	      <td data-title="\'Name\'" sortable="\'name\'" filter="{name: \'text\'}"><a ng-if="row.is_dir" ng-click="getFiles(row.name)">{[row.name]}</a><span ng-if="!row.is_dir">{[row.name]}</span></td>\
		  <td data-title="\'Extension\'" sortable="\'extension\'" filter="{extension: \'text\'}">{[row.extension]}</td>\
	   </tr>\
	 </table>'
	  );
	}]);

