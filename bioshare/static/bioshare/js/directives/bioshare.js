angular.module("bioshare-plugin",['bioshareModels','glimsModels','selectModals']);

angular.module('plugins').requires.push("bioshare-plugin");

angular.module("bioshare-plugin")
.directive('projectShare', function() {
	return {
//		restrict: 'AE',
		templateUrl: 'template/bioshare/project_share.html',
		scope: {
			project:'='
		},
		controller: function ($scope,$rootScope,$http,ProjectShare,Project,SelectModalService) {
			$scope.init = function(){
				ProjectShare.query({project:$scope.project.id},function(shares){$scope.share = shares.length == 1 ? shares[0] : null});
			}
			$scope.createShare = function(){
				var share = new ProjectShare({project:$scope.project.id});
				share.$create(function(share){$scope.share = share;})
			}
			$scope.addFiles = function(){
				SelectModalService.selectFiles('/api/projects/'+$scope.project.id+'/',{selection:$scope.share.symlinks,actions:{select:true,deselect:true}}).result.then(function(result){
					console.log('selected',result.selection,result.added,result.removed);
//					$scope.share.link_paths({paths:files});
					$http.post('/bioshare/api/project_shares/'+$scope.share.id+'/set_paths/',{paths:result.selection})
						.then(function(response){
								$scope.share.symlinks = response.data.symlinks;
								$scope.$broadcast('refresh-files');
						});
				});
			}
		}
	}
})
.run(['$templateCache', function($templateCache) {
	$templateCache.put('template/bioshare/project_share.html',
	'<load-on-select>\
			<div ng-init="init()">\
				<button ng-if="share===null" ng-click="createShare()" class="btn btn-success">Create Share</button>\
				<div ng-if="share.id">\
				<p><a href="{[share.url]}" target="_blank">View on Bioshare</a></p>\
				<button ng-click="addFiles()" class="btn btn-success pull-right">Change selection</button>\
				<h3>Linked project files</h3>\
				<list-files base-url="/bioshare/api/project_shares/{[share.id]}/" selection="share.symlinks"></list-files>\
				</div>\
			</div>\
	</load-on-select>'
	);
}]);
//
//
