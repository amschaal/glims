
angular.module('mainapp')
.controller('JobSubmissionController', ['$scope', JobSubmissionController]);

function JobSubmissionController($scope) {
	$scope.headers=[{'name':'id','label':'ID'},{'name':'name','label':'Name'},{'name':'description','label':'Description'}];
//	$scope.jobLink = function(job){return django_js_utils.urls.resolve('job', { job_id: job.job_id })};
}

