
var app = angular.module('mainapp');
app.requires.push('glims.formly');
app.controller('SampleController', ['$scope','$log','FormlyModal', 'ModelType', 'Sample',SampleController])
function SampleController($scope , $log, FormlyModal, ModelType, Sample){
	$scope.init = function (params){
		$scope.sample = Sample.get({id:params.sample});
	};
	var fields = [
					{
					    key: 'project',
					    type: 'ui-select-search',
					    templateOptions: {
					      optionsAttr: 'bs-options',
					      label: 'Project',
					      valueProp: 'id',
					      labelProp: 'name',
					      url: '/api/projects/',
					      options: []
					    }
					  },
	                {"templateOptions": {"required": false, "description": "", "label": "Name"}, "type": "input", "key": "name"}, 
	                {"templateOptions": {"required": false, "description": "", "label": "Description"}, "type": "textarea", "key": "description"},
	                {"templateOptions": {"required": false, "description": "", "label": "Received"}, "type": "input", "key": "received"}
	                ];
	$scope.editSample = function () {
    	FormlyModal.create(fields,$scope.sample,{model_type_query:{content_type__model:'sample'},title:'Edit sample',controller:'ExtendedFormlyModalController'})
    	.result.then(
    			function (sample) {
    		    	$scope.sample = sample;
    		    }
    	);
    	
    };
}
