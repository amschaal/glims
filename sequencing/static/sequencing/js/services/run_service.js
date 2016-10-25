angular.module('sequencing').requires.push('glimsServices');
angular.module('sequencing')
.service('runService', function($rootScope,$http,FormlyModal,Run,Machine,ModelType) {
	 
	 var fields =  [
	   		     {"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"},
	   		     {
					 key: 'machine',
					 type: 'ui-select-search',
					 templateOptions: {
					   optionsAttr: 'bs-options',
					   label: 'Machine',
					   valueProp: 'id',
					   labelProp: 'name',
					   url: '/sequencing/api/machines/',
					   options: []
					 }
				 },
	   			 {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"},
//	   			 {"templateOptions": {"required": false, "description": "", "label": "Received"}, "type": "input", "key": "received"}
	   			];
	 return {
		 create: create,
		 update: update
	 };

	 function update(run,options) {
		    options = angular.extend({model_type_query:{content_type__model:'run'},title:'Create run',controller:'ExtendedFormlyModalController'},options||{});
			return FormlyModal.create(fields,run || new Run({}),options);
	 }
	 function create(run,options){
		 return update(run,options)
			 .result.then(
				function (run) {
					window.location.href=$rootScope.getURL('run',{pk:run.id});
				}
				);
	 }
 });

