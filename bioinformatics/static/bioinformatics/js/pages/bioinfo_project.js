
angular.module('mainapp')
.controller('BioinfoProjectController', ['$scope','$http', 'BioinfoProject','User','$modal', BioinfoProjectController]);

function BioinfoProjectController($scope,$http,BioinfoProject,User,$modal) {
	$scope.init = function(params){
		console.log(params.id);
		$scope.project = BioinfoProject.get({id:params.id});
		$scope.project_simple = BioinfoProject.get({id:params.id,simple:true});
//		$http.get('/formly_forms/form/BioinfoProjectForm/').then(function(response){
//			$scope.fields = response.data.fields;
//			//{"fields": [{"templateOptions": {"required": false, "options": [{"name": "---------", "value": ""}, {"name": "mtbritton", "value": 2}, {"name": "jfass", "value": 3}], "description": "", "label": "Assigned to"}, "type": "select", "key": "assigned_to"}, {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"}]}
//		});
		$scope.fields = [
		                {"templateOptions": {"required": false, "options": [{"name": "---------", "value": ""}, {"name": "mtbritton", "value": 2}, {"name": "jfass", "value": 3}], "description": "", "label": "Assigned to"}
							, "type": "select", "key": "assigned_to.id"
							, expressionProperties: {
							      'data.assigned_to': 'model.assigned_to.id'
						    }
						}, 
		                 {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"
		                	 , expressionProperties: {
							      'data.description': 'model.description'
							    }
		                 }
						];
		
//		expressionProperties: {
//		      'data.assigned_to': 'model.myThing.length > 5'
//		    }
	};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab })};
	$scope.options = {};	     	    
    
    $scope.openFormlyModal = function () {
	    var modalInstance = $modal.open({
	      templateUrl: 'formlyModal.html',
	      controller: 'FormlyModalController',
	      size: 'lg',
	      resolve: {
	    	  fields: function () {
		          return $scope.fields;
		      },
		      model: function () {
		          return $scope.project;
		      }
	      }
	    });

	    modalInstance.result.then(function (data) {
	    }, function () {
	    });
	  };
}

