

angular.module('taskModels', ['ngResource'])
.factory('Task', ['$resource', function ($resource) {
	function transformTask(task){
		task.from = task.start;
    	task.to = task.end;
    	delete task['start'];
    	delete task['end'];
    	var row = {name:task.name,id:task.id,pk:task.id,tasks:[task]};
    	return row;
	}
	var transformResponse = function(data, headers){
		try {
	        var jsonObject = JSON.parse(data); // verify that json is valid
	        var rows = [];
	        angular.forEach(jsonObject.results,function(task,index){
	        	var row = transformTask(task);
	        	rows.push(row);
	        });
	        return rows;
	    }
	    catch (e) {
	        console.log("did not receive a valid Json: " + e)
	    }
	    return {};
	};
	var transformSingleResponse = function(data, headers){
		try {
	        var jsonObject = JSON.parse(data); // verify that json is valid
	        var row = transformTask(jsonObject);
	        return row;
	    }
	    catch (e) {
	        console.log("did not receive a valid Json: " + e)
	    }
	    return {};
	};
	var transformRequest = function(data,headersGetter){
		var task = data.tasks[0];
		console.log('transform task',task);
		task.start = task.from;
    	task.end = task.to;
    	delete task['from'];
    	delete task['to'];
    	return JSON.stringify(task);
	};
	return $resource('/tasks/api/tasks/:pk/', {pk:'@pk'}, {
    query: { method: 'GET', transformResponse:transformResponse, isArray:true },
    save : { method : 'PUT', transformRequest:transformRequest,transformResponse:transformSingleResponse},
    patch : { method : 'PATCH', transformRequest:transformRequest,transformResponse:transformSingleResponse},
    create : { method : 'POST',url:'/tasks/api/tasks/', transformRequest:transformRequest,transformResponse:transformSingleResponse},
    remove : { method : 'DELETE' },
  });
}]);

