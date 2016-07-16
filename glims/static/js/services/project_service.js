angular.module('glimsServices')
 .service('projectService', function($rootScope,$http,FormlyModal,Project,User,ModelType) {
	 var sample_types = ModelType.query({content_type__model:'sample'});
	 var userOptions = User.query({id__gte:1});//groups__name:'Bioinformatics Core'
	 var projectOptions = Project.query({id__gte:1});
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
					 },
					 watcher: {
			          listener: function(field, newValue, oldValue, scope, stopWatching) {
			        	  if (newValue && newValue != oldValue){
				    			console.log('model.group changed',newValue);
					    		angular.forEach(scope.fields,function(field,index){
					    			if (field.key=='participants')
					    				field.templateOptions.options = User.query({id__gte:1,groups__name:newValue.name});//;
					    		});
			        	  }
			          }
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
	   			{
	   				"templateOptions": {"required": false, "options": userOptions, "description": "", "label": "Manager","valueProp":"id","labelProp":"name" }
				, "type": "select", "key": "manager.id", data:{"error_key":"manager"}
				}, 
	             {
	            	  key: 'participants',
	            	  type: 'objectMultiCheckbox',
	            	  templateOptions: {
	            	    label: 'Participants',
	            	    options: userOptions,
	            	    valueProp: 'id',
	            	    labelProp: 'name',
	            	    required: false
	            	  }
	        	},
	        	{"templateOptions": {"required": false, "description": "", "label": "Archived"}, "type": "checkbox", "key": "archived"}
	   			];
	 return {
		 create: create,
		 update: update
	 };

	 function update(project,options) {
		    var postInit = function(scope){
		    	console.log('INITIALIZING SCOPE!!',scope);
//		    	scope.$watch('model.group',function(newValue,oldValue){
//			    		if (newValue && newValue != oldValue){
//			    			console.log('model.group changed',newValue);
//				    		angular.forEach(scope.fields,function(field,index){
//				    			if (field.key=='participants')
//				    				field.templateOptions.options = User.query({id__gte:1,groups__name:newValue.name});//;
//				    		});
//			    		}
//			    			
//	    		});
	    	}
		    
		    options = angular.extend({model_type_query:{content_type__model:'project'},title:'Create project',controller:'ExtendedFormlyModalController',postInit:postInit},options||{});
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

