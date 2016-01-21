
var app = angular.module('mainapp');
app.requires.push('glims.formly');
app.controller('BioinfoProjectController', ['$scope','$http', 'BioinfoProject','User','$modal', BioinfoProjectController]);

function BioinfoProjectController($scope,$http,BioinfoProject,User,$modal) {
	$scope.init = function(params){
		console.log(params.id);
		$scope.project = BioinfoProject.get({id:params.id});
		$scope.project_simple = BioinfoProject.get({id:params.id,simple:true});
//		$http.get('/formly_forms/form/BioinfoProjectForm/').then(function(response){
//			$scope.fields = response.data.fields;
//			//{"fields": [{"templateOptions": {"required": false, "options": [{"name": "---------", "value": ""}, {"name": "mtbritton", "value": 2}, {"name": "jfass", "value": 3}], "description": "", "label": "Assigned to"}, "type": "select", "key": "assigned_to"}, {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"}]}
//		});
//		var userOptions = [{"name": "---------", "value": ""}, {"name": "mtbritton", "value": 2}, {"name": "jfass", "value": 3}];
//		var userOptions = [
//		                 {'first_name': 'Monica', 'last_name': 'Britton', 'email': '', 'groups': [1], 'id': 2},
//		                 {'first_name': 'Joe', 'last_name': 'Fass', 'email': '', 'groups': [1], 'id': 3}
//		                ]
		var userOptions = User.query({groups__name:'Bioinformatics Core'});//BioinfoProject.users({search:name});
		$scope.fields = [
						{"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"
						}, 
		                {"templateOptions": {"required": false, "options": userOptions, "description": "", "label": "Manager","valueProp":"id","labelProp":"first_name" }
							, "type": "select", "key": "manager.id", data:{"error_key":"manager"}
						}, 
		                 {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"
		                 },
		                 {
		                	  key: 'participants',
		                	  type: 'objectMultiCheckbox',
		                	  templateOptions: {
		                	    label: 'Participants',
		                	    options: userOptions,
		                	    valueProp: 'id',
		                	    labelProp: 'first_name'
		                	  }
	                	}
//		                 {
//		                     key: 'participants',
//		                     type: 'ui-select-multiple-search',
//		                     templateOptions: {
//		                       ngOptions: 'option in to.options | filter: $select.search',//option[to.valueProp] as option in to.options | filter: $select.search
//		                       optionsAttr: 'bs-options',
//		                       label: 'Participants',
//		                       valueProp: 'id',
//		                       labelProp: 'first_name',
//		                       labelFunc: function(item,to){return item.first_name + ' ' + item.last_name;},
//		                       placeholder: 'Select options',
////		                       options: userOptions
//		                       options: [],
//		                       refresh: refreshUsers,
//		                       refreshDelay: 0
//		                     }
//		                   }
						];
		 function refreshUsers(name, field) {
			 console.log(name,field);
			  return  BioinfoProject.users({search:name}).$promise.then(function(users){
				  console.log('users',users);
				  field.templateOptions.options = users;
			  });
//				 [
//	                 {'first_name': 'Monica', 'last_name': 'Britton', 'email': '', 'groups': [1], 'id': 2},
//	                 {'first_name': 'Joe', 'last_name': 'Fass', 'email': '', 'groups': [1], 'id': 3}
//	                ];
////				 [
//	                 {'first_name': 'asdf', 'last_name': 'Britton', 'email': '', 'groups': [1], 'id': 2},
//	                 {'first_name': 'Jassdoe', 'last_name': 'Fass', 'email': '', 'groups': [1], 'id': 3}
//	                ];
//             var promise;
//             if (!address) {
//               promise = $q.when({data: {results: []}});
//             } else {
//               var params = {address: address, sensor: false};
//               var endpoint = '//maps.googleapis.com/maps/api/geocode/json';
//               promise = $http.get(endpoint, {params: params});
//             }
//             return promise.then(function(response) {
//               field.templateOptions.options = response.data.results;
//             });
           }
		
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
		          return angular.copy($scope.project);
		      },
		      options: function(){
		    	  return {title:'Edit project'};
		      }
	      }
	    });

	    modalInstance.result.then(function (project) {
	    	$scope.project = project;
	    }, function () {
	    });
	  };
}

