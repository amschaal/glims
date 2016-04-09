angular.module('glimsServices')
 .service('poolService', function($rootScope,$http,FormlyModal,Pool,ModelType) {
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
	   		     {"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"}, 
	   			 {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"},
	   			];
	 return {
		 create: create,
		 update: update
	 };

	 function update(pool,options) {
		    options = angular.extend({model_type_query:{content_type__model:'pool'},title:'Create pool',controller:'ExtendedFormlyModalController'},options||{});
			return FormlyModal.create(fields,pool || new Pool({}),options);
			
	 }
	 function create(pool,options){
//		 pool = pool || new Pool();
		 return update(pool,options)
			 .result.then(
				function (pool) {
					window.location.href=$rootScope.getURL('pool',{pk:pool.id});
				}
				);
	 }
 });

