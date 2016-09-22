angular.module("project", ["project.tpls","project.directives"]);
angular.module("project.tpls", ["template/project/archive.html"]);

angular.module('project.directives', ['glimsModels','angular-growl'])
.directive('archiveProject', function(Project,growl) {
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
	    			growl.success('Project "'+$scope.project.name+'" archived',{ttl: 4000});
	    		},function(){
	    			$scope.project.archived=false;
	    			growl.error('Error archiving project "'+$scope.project.name+'"',{ttl: 4000});
	    		});
	    	}
	    	$scope.unarchive = function (){
	    		$scope.project.archived = false;
	    		$scope.project.$save(function(){
	    			growl.success('Project "'+$scope.project.name+'" unarchived',{ttl: 4000});
	    		},function(){
	    			$scope.project.archived=true;
	    			growl.error('Error unarchiving project "'+$scope.project.name+'"',{ttl: 4000});
	    		});
	    	}
	    }
	  }
	});


angular.module('template/project/archive.html', []).run(['$templateCache', function($templateCache) {
	  $templateCache.put('template/project/archive.html',
	'<button ng-click="archive()" ng-if="project && !project.archived" class="btn btn-default btn-sm btn-success"><i class="fa fa-folder-open-o" aria-hidden="true"></i> Archive</button><button ng-click="unarchive()" ng-if="project && project.archived" class="btn btn-default btn-sm btn-warning"><i class="fa fa-folder-o" aria-hidden="true"></i> Unarchive</button>'
	  );
	}]);

