angular.module('glimsServices')
 .service('libraryService', function($rootScope,$http,FormlyModal,Library,User,ModelType) {
//	 var sample_types = ModelType.query({content_type__model:'sample'});
	 var fields =  [
	            {"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"}, 
				{"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"},
	            {
					 key: 'sample',
					 type: 'ui-select-search',
					 templateOptions: {
					   optionsAttr: 'bs-options',
					   label: 'Sample',
					   valueProp: 'id',
					   labelProp: 'name',
					   url: '/api/samples/',
					   options: []
					 }
				 },
				 {
					 key: 'adapter',
					 type: 'ui-select-search',
					 templateOptions: {
					   optionsAttr: 'bs-options',
					   label: 'Adapter',
					   valueProp: 'id',
					   labelProp: 'name',
					   url: '/api/adapters/',
					   options: []
					 }
				 },
//	   			 {
//	   				  key: 'sample_type',
//	   				  type: 'select',
//	   				  templateOptions: {
//	   				    label: 'Sample Type',
//	   				    ngOptions: "option as option.name for option in to.options track by option.id",
//	   				    options: sample_types,
//	   				    valueProp: 'id',
//	   				    labelProp: 'name'
//	   				  }
//	   			 },
	   			];
	 return {
		 create: create,
		 update: update
	 };

	 function update(library,options) {
		    options = angular.extend({model_type_query:{content_type__model:'library'},title:'Create library',controller:'ExtendedFormlyModalController'},options||{});
			return FormlyModal.create(fields,library || new Library({}),options);
			
	 }
	 function create(library,options){
		 return update(library,options);
//			 .result.then(
//				function (library) {
////					window.location.href=$rootScope.getURL('library',{pk:library.id});
//				}
//			);
	 }
 });

