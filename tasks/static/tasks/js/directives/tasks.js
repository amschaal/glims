angular.module("tasks-plugin", ['taskModels','angularMoment','gantt', 'gantt.table', 'gantt.movable', 'gantt.tooltips']);

angular.module('plugins').requires.push("tasks-plugin")

angular.module("tasks-plugin")
.directive('tasksPlugin', function(Task) {
	return {
		restrict: 'AE',
		templateUrl: 'template/plugins/tasks.html',
		scope: {
			objectId:'=',
			contentType:'=',
			getURL:'&'
		},
		controller: function ($scope,$rootScope,$http,$log,$uibModal) {
			console.log('task plugin',$scope);
			$scope.getURL = $rootScope.getURL;
			$scope.tasks = Task.query({});
			$scope.saveTasks = function(){
				angular.forEach($scope.tasks,function(task,index){
					if (!task.create)
						task.$save();
					else{
						delete task['id'];
						task.$create();
					}
						
					console.log('save task',task);
				});
			}
			$scope.addTask = function(task){
				task.project = $scope.objectId;
				$scope.tasks.push(new Task({name:task.name,create:true,tasks:[task]}));
			}
//			$scope.tasks = [{name: 'tasks', height: '3em', sortable: false, classes: 'gantt-row-task', color: '#45607D', tasks: [
//			                                                                                                                                    // Dates can be specified as string, timestamp or javascript date object. The data attribute can be used to attach a custom object
//			                                                                                                                                    {name: 'Kickoff', color: '#93C47D', from: '2013-10-07T09:00:00', to: '2013-10-07T10:00:00', data: 'Can contain any custom data or object'},
//			                                                                                                                                    {name: 'Concept approval', color: '#93C47D', from: new Date(2013, 9, 18, 18, 0, 0), to: new Date(2013, 9, 18, 18, 0, 0), est: new Date(2013, 9, 16, 7, 0, 0), lct: new Date(2013, 9, 19, 0, 0, 0)},
//			                                                                                                                                    {name: 'Development finished', color: '#93C47D', from: new Date(2013, 10, 15, 18, 0, 0), to: new Date(2013, 10, 15, 18, 0, 0)},
//			                                                                                                                                    {name: 'Shop is running', color: '#93C47D', from: new Date(2013, 10, 22, 12, 0, 0), to: new Date(2013, 10, 22, 12, 0, 0)},
//			                                                                                                                                    {name: 'Go-live', color: '#93C47D', from: new Date(2013, 10, 29, 16, 0, 0), to: new Date(2013, 10, 29, 16, 0, 0)}
//			                                                                                                                                ], data: 'Can contain any custom data or object'},
//			                                                                                                                                {name: 'Status meetings', tasks: [
//			                                                                                                                                    {name: 'Demo #1', color: '#9FC5F8', from: new Date(2013, 9, 25, 15, 0, 0), to: new Date(2013, 9, 25, 18, 30, 0)},
//			                                                                                                                                    {name: 'Demo #2', color: '#9FC5F8', from: new Date(2013, 10, 1, 15, 0, 0), to: new Date(2013, 10, 1, 18, 0, 0)},
//			                                                                                                                                    {name: 'Demo #3', color: '#9FC5F8', from: new Date(2013, 10, 8, 15, 0, 0), to: new Date(2013, 10, 8, 18, 0, 0)},
//			                                                                                                                                    {name: 'Demo #4', color: '#9FC5F8', from: new Date(2013, 10, 15, 15, 0, 0), to: new Date(2013, 10, 15, 18, 0, 0)},
//			                                                                                                                                    {name: 'Demo #5', color: '#9FC5F8', from: new Date(2013, 10, 24, 9, 0, 0), to: new Date(2013, 10, 24, 10, 0, 0)}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Kickoff', movable: {allowResizing: false}, tasks: [
//			                                                                                                                                    {name: 'Day 1', color: '#9FC5F8', from: new Date(2013, 9, 7, 9, 0, 0), to: new Date(2013, 9, 7, 17, 0, 0),
//			                                                                                                                                        progress: {percent: 100, color: '#3C8CF8'}, movable: false},
//			                                                                                                                                    {name: 'Day 2', color: '#9FC5F8', from: new Date(2013, 9, 8, 9, 0, 0), to: new Date(2013, 9, 8, 17, 0, 0),
//			                                                                                                                                        progress: {percent: 100, color: '#3C8CF8'}},
//			                                                                                                                                    {name: 'Day 3', color: '#9FC5F8', from: new Date(2013, 9, 9, 8, 30, 0), to: new Date(2013, 9, 9, 12, 0, 0),
//			                                                                                                                                        progress: {percent: 100, color: '#3C8CF8'}}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Create concept', tasks: [
//			                                                                                                                                    {name: 'Create concept', content: '<i class="fa fa-cog" ng-click="scope.handleTaskIconClick(task.model)"></i> {[task.model.name]}', color: '#F1C232', from: new Date(2013, 9, 10, 8, 0, 0), to: new Date(2013, 9, 16, 18, 0, 0), est: new Date(2013, 9, 8, 8, 0, 0), lct: new Date(2013, 9, 18, 20, 0, 0),
//			                                                                                                                                        progress: 100}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Finalize concept', tasks: [
//			                                                                                                                                    {name: 'Finalize concept', color: '#F1C232', from: new Date(2013, 9, 17, 8, 0, 0), to: new Date(2013, 9, 18, 18, 0, 0),
//			                                                                                                                                        progress: 100}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Development', children: ['Sprint 1', 'Sprint 2', 'Sprint 3', 'Sprint 4'], content: '<i class="fa fa-file-code-o" ng-click="scope.handleRowIconClick(row.model)"></i> {[row.model.name]}'},
//			                                                                                                                                {name: 'Sprint 1', tooltips: false, tasks: [
//			                                                                                                                                    {name: 'Product list view', color: '#F1C232', from: new Date(2013, 9, 21, 8, 0, 0), to: new Date(2013, 9, 25, 15, 0, 0),
//			                                                                                                                                        progress: 25}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Sprint 2', tasks: [
//			                                                                                                                                    {name: 'Order basket', color: '#F1C232', from: new Date(2013, 9, 28, 8, 0, 0), to: new Date(2013, 10, 1, 15, 0, 0)}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Sprint 3', tasks: [
//			                                                                                                                                    {name: 'Checkout', color: '#F1C232', from: new Date(2013, 10, 4, 8, 0, 0), to: new Date(2013, 10, 8, 15, 0, 0)}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Sprint 4', tasks: [
//			                                                                                                                                    {name: 'Login & Signup & Admin Views', color: '#F1C232', from: new Date(2013, 10, 11, 8, 0, 0), to: new Date(2013, 10, 15, 15, 0, 0)}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Hosting'},
//			                                                                                                                                {name: 'Setup', tasks: [
//			                                                                                                                                    {name: 'HW', color: '#F1C232', from: new Date(2013, 10, 18, 8, 0, 0), to: new Date(2013, 10, 18, 12, 0, 0)}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Config', tasks: [
//			                                                                                                                                    {name: 'SW / DNS/ Backups', color: '#F1C232', from: new Date(2013, 10, 18, 12, 0, 0), to: new Date(2013, 10, 21, 18, 0, 0)}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Server', parent: 'Hosting', children: ['Setup', 'Config']},
//			                                                                                                                                {name: 'Deployment', parent: 'Hosting', tasks: [
//			                                                                                                                                    {name: 'Depl. & Final testing', color: '#F1C232', from: new Date(2013, 10, 21, 8, 0, 0), to: new Date(2013, 10, 22, 12, 0, 0), 'classes': 'gantt-task-deployment'}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Workshop', tasks: [
//			                                                                                                                                    {name: 'On-side education', color: '#F1C232', from: new Date(2013, 10, 24, 9, 0, 0), to: new Date(2013, 10, 25, 15, 0, 0)}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Content', tasks: [
//			                                                                                                                                    {name: 'Supervise content creation', color: '#F1C232', from: new Date(2013, 10, 26, 9, 0, 0), to: new Date(2013, 10, 29, 16, 0, 0)}
//			                                                                                                                                ]},
//			                                                                                                                                {name: 'Documentation', tasks: [
//			                                                                                                                                    {name: 'Technical/User documentation', color: '#F1C232', from: new Date(2013, 10, 26, 8, 0, 0), to: new Date(2013, 10, 28, 18, 0, 0)}
//			                                                                                                                                ]}];
		}
	}
});


angular.module("tasks-plugin").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/plugins/tasks.html',
			'<div class="blah">\
			{[tasks]}\
			<load-on-select>\
			<div gantt data="tasks">\
			  <gantt-table></gantt-table>\
			  <gantt-movable></gantt-movable>\
			  <gantt-tooltips></gantt-tooltips>\
			</div>\
			<button ng-click="saveTasks()" class="btn">Save</button>\
			<p class="input-group col-4">\
			Start: <input type="text" class="form-control" uib-datepicker-popup ng-model="task.from" is-open="open_start" ng-required="true" close-text="Close" />\
			<span class="input-group-btn">\
			  <button type="button" class="btn btn-default" ng-click="open_start=true;"><i class="glyphicon glyphicon-calendar"></i></button>\
			</span>\
			</p>\
			<p class="input-group col-4">\
			Finish: <input type="text" class="form-control" uib-datepicker-popup ng-model="task.to" is-open="open_to" ng-required="true" close-text="Close" />\
			<span class="input-group-btn">\
			  <button type="button" class="btn btn-default" ng-click="open_to=true;"><i class="glyphicon glyphicon-calendar"></i></button>\
			</span>\
			<input ng-model="task.name"/>\
			<button ng-click="addTask(task)">Add</button>\
			</p>\
			</load-on-select></div>'
	);
}]);


