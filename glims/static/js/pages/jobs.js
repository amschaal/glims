
angular.module('mainapp')
.controller('JobController', ['$scope','$http', JobController]);

function JobController($scope,$http) {
	$scope.headers=[{'name':'id','label':'ID'},{'name':'status','label':'Status'},{'name':'created','label':'Created'},{'name':'description','label':'Description'}];
	$scope.link = function(job){return django_js_utils.urls.resolve('job', { id: job.id })};
	$scope.terminate = function(job){
		var url = django_js_utils.urls.resolve('terminate_job', { job_id: job.id })
		$http.post(url,{})
			.success(function(){job.status="TERMINATED"})
			.error(function(data){console.log(data)});
	};
	$scope.run = function(job){
		var url = django_js_utils.urls.resolve('run_job', { job_id: job.id })
		$http.post(url,{})
			.success(function(){job.status="STARTED"})
			.error(function(data){console.log(data)});
	};
}

