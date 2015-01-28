
angular.module('mainapp')
.controller('WorkflowController', ['$scope', WorkflowController]);

function WorkflowController($scope) {
	$scope.headers=[{'name':'created','label':'Created'},{'name':'name','label':'Name'},{'name':'type','label':'Type'},{'name':'description','label':'Description'}];
	$scope.workflowLink = function(workflow){return django_js_utils.urls.resolve('workflow', { pk: workflow.id })};
}

