angular.module('glimsServices')
 .service('BioinfoProjectService', function($rootScope,$http,FormlyModal,User,BioinfoProject,ModelType) {
		var userOptions = User.query({groups__name:'Bioinformatics Core'});//BioinfoProject.users({search:name});
		var fields = [
						{"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"}, 
						{
				   			 key: 'project',
				   			 type: 'ui-select-search',
				   			 templateOptions: {
				   			   optionsAttr: 'bs-options',
				   			   label: 'Project',
				   			   valueProp: 'id',
				   			   labelProp: 'name',
				   			   url: '/api/projects/',
				   			   options: [],
				   			   required: false
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
			   			   options: [],
			   			   required: false
			   			 }
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
		                	    labelProp: 'first_name',
		                	    required: false
		                	  }
	                	},
	                	{"templateOptions": {"required": false, "description": "", "label": "Data location"}, "type": "input", "key": "data_location"},
	                	{"templateOptions": {"required": false, "description": "", "label": "Archived"}, "type": "checkbox", "key": "archived"}
         ];
	 return {
		 create: create,
		 update: update
	 };

	 function update(bioinfo_project,options) {
		    options = angular.extend({model_type_query:{content_type__model:'bioinfoproject'},title:'Update project',controller:'ExtendedFormlyModalController'},options||{});
			return FormlyModal.create(fields,bioinfo_project || new BioinfoProject({}),options);
	 }
	 function create(bioinfo_project,options){
		 return update(bioinfo_project,options)
			 .result.then(
				function (bioinfo_project) {
					window.location.href=$rootScope.getURL('bioinformatics__project',{pk:bioinfo_project.id});
				}
				);
	 }
 });

