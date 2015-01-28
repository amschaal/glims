
angular.module('mainapp')
.controller('JobController', ['$scope', JobController]);

function JobController($scope) {
	$scope.headers=[{'name':'job_id','label':'ID'},{'name':'created','label':'Created'},{'name':'name','label':'Name'},{'name':'type','label':'Type'},{'name':'description','label':'Description'},{'name':'status','label':'Status'}];
	$scope.jobLink = function(job){return django_js_utils.urls.resolve('job', { job_id: job.job_id })};
}

