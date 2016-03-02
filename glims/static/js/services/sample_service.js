angular.module('glimsServices')
 .service('sampleService', function($rootScope,$http,FormlyModal,Sample,ModelType) {
	 var fields =  [
	   		     {"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"}, 
	   			 {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"},
	   			 {"templateOptions": {"required": false, "description": "", "label": "Received"}, "type": "input", "key": "received"}
	   			];
	 return {
		 create: create,
		 update: update
	 };

	 function update(sample,options) {
		    options = angular.extend({model_type_query:{content_type__model:'sample'},title:'Create sample',controller:'ExtendedFormlyModalController'},options||{});
			return FormlyModal.create(fields,sample || new Sample({}),options);
			
	 }
	 function create(sample,options){
		 return update(sample,options)
			 .result.then(
				function (sample) {
					window.location.href=$rootScope.getURL('sample',{pk:sample.id});
				}
				);
	 }
 });

