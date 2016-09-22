angular.module("project", ["project.tpls","project.directives"]);
angular.module("project.tpls", ["template/project/archive.html"]);

angular.module('project.directives', ["glimsModels"])
.directive('archiveProject', function(Project) {
	  return {
	    restrict: 'AE',
	    templateUrl: 'template/project/archive.html',
	    scope: {
	    	project:'='
	    },
	    controller: function($scope, $http, $element){
	    	this.$scope = $scope;
	    	$scope.archive = function (){
	    		$scope.project.archived = true;
	    		$scope.project.$save(function(){
	    			alert('archived');
	    		})
	    	}
	    	$scope.unarchive = function (){
	    		$scope.project.archived = false;
	    		$scope.project.$save(function(){
	    			alert('unarchived');
	    		})
	    	}
	    }
	  }
	});


angular.module('template/project/archive.html', []).run(['$templateCache', function($templateCache) {
	  $templateCache.put('template/project/archive.html',
	'<button ng-click="archive()" ng-if="project && !project.archived" class="btn btn-default btn-sm">Archive</button><button ng-click="unarchive()" ng-if="project && project.archived" class="btn btn-default btn-sm">Unarchive</button>'
	  );
	}]);

