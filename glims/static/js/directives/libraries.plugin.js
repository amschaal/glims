
angular.module("libraries-plugin", ['glims.formly','glimsModels','glimsServices','ngTable']);

angular.module('plugins').requires.push("libraries-plugin")

angular.module("libraries-plugin")
.directive('sampleLibraries', function(Sample,Library,Adapter,libraryService) {
	return {
		restrict: 'AE',
		templateUrl: 'template/plugins/sample_libraries.html',
		scope: {
			sample:'=',
//			getURL:'&'
		},
		controller: function ($scope,$rootScope,$http,$log,$uibModal,NgTableParams) {
			$scope.getURL = $rootScope.getURL;
			$scope.errors = false;
			$scope.adapters = Adapter.query();
			function updateLibraryCount(){
				$rootScope.library_count = $scope.libraries ? $scope.libraries.length : 0;
			}
			$scope.refreshLibraries = function(){
				console.log('refreshing libraries',$scope.sample);
				$scope.libraries = Library.query({sample:$scope.sample.id},function() {
					$scope.tableParams = new NgTableParams({}, {
					      dataset: $scope.libraries
					    });
					updateLibraryCount()
				});
			}
			$scope.$watch('sample.id',function(newValue,oldValue){
				if (newValue)
					$scope.refreshLibraries();
			});
			$scope.createLibrary = function(){
				libraryService.create(new Library({sample:$scope.sample})).result.then(
						function(library){
							console.log('library',library);$scope.libraries.push(library);
							$scope.tableParams.reload()
						});
			}
			$scope.editLibrary = function(library){
				libraryService.update(library).result.then(
						function(updated_library){
							var index = $scope.libraries.indexOf(library);
							$scope.libraries[index]=updated_library;
							$scope.tableParams.reload();
						});
			}
			$scope.deleteLibrary = function(library,index){
				if (!confirm('Are you sure you want to delete this library?'))
					return;
				library.$delete(function(){
					var index = $scope.libraries.indexOf(library);
					$scope.libraries.splice(index,1);
					$scope.tableParams.reload();
				},function(){
					
				})
			}
		}

	}
});


angular.module("libraries-plugin").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/plugins/sample_libraries.html',
			'<load-on-select>\
			<button ng-click="createLibrary()" class="btn btn-success btn-sm">Create Library</button>\
			<table ng-table="tableParams" class="table table-condensed table-bordered table-striped">\
		      <tr ng-repeat="row in $data">\
				<td data-title="\'Created\'" sortable="\'created\'">{[row.created|date]}</td>\
				<td data-title="\'Name\'" filter="{name: \'text\'}" sortable="\'name\'">{[row.name]}</td>\
		        <td data-title="\'Adapter\'" filter="{\'adapter.name\': \'text\'}" sortable="\'adapter.name\'">{[row.adapter.name]}</td>\
		        <td data-title="\'Description\'" filter="{description: \'text\'}" sortable="\'description\'">{[row.description]}</td>\
				<td data-title="\'Pools\'"><a href="{[getURL(\'pool\',{pk:p.id})]}" ng-repeat="p in row.pools">{[p.name]}{[$last ? \'\' : \', \']}</a></td>\
		        <td data-title="\'Actions\'"><button class="btn btn-sm btn-primary" ng-click="editLibrary(row)">Edit</button> <button class="btn btn-sm btn-danger" ng-click="deleteLibrary(row,$index)">Delete</button></td>\
		      </tr>\
		    </table>\
			</load-on-select>'
	);
}]);

