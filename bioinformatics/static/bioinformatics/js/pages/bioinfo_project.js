
var app = angular.module('mainapp');
app.requires.push('glims.formly');
app.controller('BioinfoProjectController', ['$scope','$http', 'BioinfoProject','User','FormlyModal', BioinfoProjectController]);

function BioinfoProjectController($scope,$http,BioinfoProject,User,FormlyModal) {
	$scope.init = function(params){
		console.log(params.id);
		$scope.project = BioinfoProject.get({id:params.id});
		$scope.project_simple = BioinfoProject.get({id:params.id,simple:true});
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
           }
		
	};
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab })};
	$scope.options = {};	     	    
    
    $scope.openFormlyModal = function () {
    	FormlyModal.create($scope.fields,$scope.project,{title:'Edit project'})
    	.result.then(
    			function (project) {
    		    	$scope.project = project;
    		    }
    	);
    	
    };
}

