angular.module('glimsServices')
 .service('projectService', function($rootScope,$http,FormlyModal,Project,User,ModelType) {
	 var sample_types = ModelType.query({content_type__model:'sample'});
	 var userOptions = {}//Used for caching
	 function getUserOptions($viewValue,$modelValue,scope){
		 if (scope.model.group){
			 //cache options
			 if (!userOptions[scope.model.group.id])
				 userOptions[scope.model.group.id] = User.query({groups__id:scope.model.group.id});
			 return userOptions[scope.model.group.id];
		 }
			 
	 }
	 var fields =  [
	            {
					 key: 'group',
					 type: 'ui-select-search',
					 templateOptions: {
					   optionsAttr: 'bs-options',
					   label: 'Group',
					   valueProp: 'id',
					   labelProp: 'name',
					   url: '/api/groups/',
					   options: []
					 }
				 },
				 {
		   			 key: 'related_projects',
		   			 type: 'ui-select-search-multiple',
		   			 templateOptions: {
		   			   optionsAttr: 'bs-options',
		   			   label: 'Related Projects',
		   			   valueProp: 'id',
		   			   labelProp: 'name',
		   			   url: '/api/projects/',
		   			   options: []
		   			 }
		   			},
	   		     {"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"}, 
	   			 {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"},
	   			 {
	   				  key: 'sample_type',
	   				  type: 'select',
	   				  templateOptions: {
	   				    label: 'Sample Type',
	   				    ngOptions: "option as option.name for option in to.options track by option.id",
	   				    options: sample_types,
	   				    valueProp: 'id',
	   				    labelProp: 'name'
	   				  }
	   			 },
	   			 {
	   			 key: 'lab',
	   			 type: 'ui-select-search',
	   			 templateOptions: {
	   			   optionsAttr: 'bs-options',
	   			   label: 'Lab',
	   			   valueProp: 'id',
	   			   labelProp: 'name',
	   			   url: '/api/labs/',
	   			   options: []
	   			 }
	   			},
	   			{"templateOptions": {"required": false, "description": "", "label": "Contact"}, "type": "textarea", "key": "contact"},
	   			{
	   				"templateOptions": {
	   					"required": false, 
	   					"description": "", 
	   					"label": "Manager",
	   					"valueProp":"id",
	   					"labelProp":"name",
	   					},
   					expressionProperties:{
	            		  'templateOptions.options':getUserOptions
   					},
   					"type": "select", 
   					"key": "manager.id", 
   					"data":{"error_key":"manager"}
				}, 
	             {
	            	  key: 'participants',
	            	  type: 'objectMultiCheckbox',
	            	  templateOptions: {
	            	    label: 'Participants',
//	            	    options: userOptions,
	            	    valueProp: 'id',
	            	    labelProp: 'name',
	            	    required: false
	            	  },
	            	  expressionProperties:{
	            		  'templateOptions.options':getUserOptions
	            	  }
	        	},
	        	{"templateOptions": {"required": false, "description": "", "label": "Archived"}, "type": "checkbox", "key": "archived"},
//	        	{
//	        		"expressionProperties":{
//	            		  'templateOptions.form_fields':getTypeFields
//	            	  },
//                     "type": "subForm", "key": "data"
//                }
	   			];
	 return {
		 create: create,
		 update: update
	 };

	 function update(project,options) {
		    options = angular.extend({model_type_query:{content_type__model:'project'},title:'Create project',controller:'ExtendedFormlyModalController'},options||{});
			return FormlyModal.create(fields,project || new Project({}),options);
			
	 }
	 function create(project,options){
		 return update(project,options)
			 .result.then(
				function (project) {
					window.location.href=$rootScope.getURL('project',{pk:project.id});
				}
				);
	 }
 });

