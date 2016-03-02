angular.module('glimsServices')
 .service('projectService', function($rootScope,$http,FormlyModal,Project,ModelType) {
	 var sample_types = ModelType.query({content_type__model:'sample'});
	 var fields =  [

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
	   			}
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

