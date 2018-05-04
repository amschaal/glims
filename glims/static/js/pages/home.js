
var app = angular.module('mainapp');
app.controller('HomeController', ['$scope','$window','$http','LocationSearchState','DRFNgTableParams', HomeController]);

function HomeController($scope,$window,$http,LocationSearchState,DRFNgTableParams) {
	$scope.projectLink = function(id){return django_js_utils.urls.resolve('project', { pk: id })};
//	$scope.tableSettings = {sorting: { modified: "desc" },filter:{archived:'False',following:true}};
	$scope.issueTableParams = DRFNgTableParams('/api/notes/',{sorting: { created: "desc" },filter:{tags:'issue',not_tags:'closed',following:true}});
//	$scope.userProfile.$promise.then(function(profile){
//		console.log('profile',profile);
//		if (_.has(profile,'preferences.pages.projects.tableSettings.filter'))
//			$scope.tableSettings.filter = profile.preferences.pages.projects.tableSettings.filter;
//		if (_.has(profile,'preferences.pages.projects.tableSettings.sorting'))
//			$scope.tableSettings.sorting = profile.preferences.pages.projects.tableSettings.sorting;
//		if (_.has(profile,'preferences.pages.projects.tableSettings.cols'))
//			angular.extend($scope.cols,profile.preferences.pages.projects.tableSettings.cols);
//		console.log('tableSettings',$scope.tableSettings);
//		$scope.loadState();
//		$scope.tableParams = DRFNgTableParams('/api/projects/',$scope.tableSettings ,Project);
//	});
//	$scope.saveFilters = function(){
//		_.set($scope.userProfile,'preferences.pages.projects.tableSettings.filter',$scope.tableParams.filter());
//		_.set($scope.userProfile,'preferences.pages.projects.tableSettings.sorting',$scope.tableParams.sorting());
//		_.set($scope.userProfile,'preferences.pages.projects.tableSettings.cols',$scope.cols);
//		$scope.save_disabled = true;
//		$scope.saveProfileText = 'Saving...';
//		$scope.userProfile.$save(
//			function(){$scope.save_disabled=false;$scope.saveProfileText = null;growl.success("Savings saved",{ttl: 3000})},
//			function(){$scope.save_disabled=false;$scope.saveProfileText = null;growl.error("Error saving settings",{ttl: 3000})}
//		);
//	};
//	$scope.changeFilter = function(field, value){
//	      var filter = {};
//	      filter[field] = value;
//	      angular.extend($scope.tableParams.filter(), filter);
//	};
//	$scope.updateFilters = function(){
//		console.log('filter',$scope.tableSettings.filter)
//		$scope.tableParams.filter($scope.tableSettings.filter);
//	};
//	$scope.saveStatus = function(project){
//		console.log('project',project);
//		project.status = project.new_status.id;
//	};
//	$scope.loadState = function(){
//		var state = LocationSearchState.get();
//		if (state.cols)
//			for (var key in state.cols){
//				$scope.cols[key] = typeof(state.cols[key]) === "boolean" ? state.cols[key] : (state.cols[key].toLowerCase() === "true");
//			}
//		if (state.tableSettings)
//			$scope.tableSettings = state.tableSettings; 
//	};
//	$scope.saveState = function(){
//		var url_params = $scope.tableParams.url();
//		var state = {tableSettings:{page:url_params.page,count:url_params.count,sorting:$scope.tableParams.sorting(),filter:$scope.tableParams.filter()},cols:$scope.cols};
//		LocationSearchState.set(state);
//	};
//	$window.addEventListener('onbeforeunload', function(e) {
//		alert('hello');
//		saveState();
//    });
}