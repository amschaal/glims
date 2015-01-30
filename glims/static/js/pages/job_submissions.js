
angular.module('mainapp')
.controller('JobSubmissionController', ['$scope', JobSubmissionController]);

function JobSubmissionController($scope) {
	$scope.headers=[{'name':'id','label':'ID'},{'name':'name','label':'Name'},{'name':'description','label':'Description'}];
	$scope.link = function(submission){return django_js_utils.urls.resolve('job_submission', { id: submission.id })};
}

