
angular.module('Dashboard')
.controller('StudyController', ['$scope', StudyController]);

function StudyController($scope) {
	$scope.headers=[{'name':'name','label':'Name'},{'name':'group','label':'PI'},{'name':'description','label':'Description'}];
	$scope.permissionLink = function(study){return django_js_utils.urls.resolve('permissions', { model: 'study', pk: study.id })};
	$scope.studyLink = function(study){return django_js_utils.urls.resolve('study', { pk: study.id })};
}

