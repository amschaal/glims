angular.module('formly.modal',[])
.config(function (formlyConfigProvider) {

    formlyConfigProvider.setWrapper({
      name: 'validation',
      types: ['input','textarea','select'],
      template: '<formly-transclude></formly-transclude>\
				  <div class="my-messages help-block" ng-messages="fc.$error" ng-if="options.formControl.$touched">\
				    <div class="some-message" ng-message="{[::name]}" ng-repeat="(name, message) in ::options.validation.messages">\
				      {[message(fc.$viewValue, fc.$modelValue, this)]}\
				    </div>\
				  </div>'
    });

  })
.service('FormlyModal',function($modal){
	return {
		create:create
	};
	function create(fields,model,options){
	var modalInstance = $modal.open({
	      template: '	<div class="modal-header">\
	          <h3 class="modal-title">{[title]}</h3>\
	          </div>\
	          <div class="modal-body">\
	  			<form ng-submit="onSubmit()" name="form" novalidate>\
	  		        <formly-form model="model" ng-model-options="{ allowInvalid: true }" fields="fields" options="options" form="form">\
	  		          <button type="submit" class="btn btn-primary submit-button">Submit</button>\
	  		          <button type="button" class="btn btn-default" ng-click="options.resetModel()">Reset</button>\
	  		        </formly-form>\
	  		      </form>\
	          </div>\
	          <div class="modal-footer">\
	              <button class="btn btn-warning" ng-click="cancel()">Cancel</button>\
	          </div>',
	      controller: options.controller||'FormlyModalController',
	      size: 'lg',
	      resolve: {
	    	  fields: function () {
		          return fields;
		      },
		      model: function () {
		          return options.by_reference ? model : angular.copy(model);
		      },
		      options: function(){
		    	  return options||{title:'Edit!!'};
		      }
	      }
	    });
	    modalInstance.result.then(options.success||function(model){console.log(model);},options.error||function(){});
	    return modalInstance;
	}
})
.service('FormlyDynamicFields',function($modal){
	return {
		translateField:translateField,
		translateFields:translateFields
	};
	function translateFieldType(type){
		switch (type){
			case 'checkbox':
				return 'checkbox';
			case 'select':
				return 'select';
			default:
				return 'input';
		}
	}
	function translateField(field){
		var field_description = {
			    "key": "data."+field.name,
			    "type": translateFieldType(field.type),
			    "templateOptions": {
			      "label": field.label,
			      "required": field.required
				    }
				};
		if (field_description.type == 'select'){
			
			field_description.templateOptions.options = field.choices.map(function(obj){
				var choice = {'name':obj.name||obj.value,'value':obj.value||obj.name};
//				console.log('choice',choice);
				return choice;
			});
//			console.log('select',field,field_description);
		}
		return field_description;
		
//		return field;
	}
	function translateFields(fields){
		var translated = [];
		angular.forEach(fields,function(field,index){
			translated.push(translateField(field));
		});
		return translated;
	}
})
.controller('FormlyModalController', function FormlyModalController($scope, $http, $modalInstance, fields, model, options) {
	$scope.model = model;
	$scope.options = {};
	fields = angular.copy(fields);
	$scope.title = options.title ? options.title : 'Edit';
	if (options.exclude){
		angular.forEach(fields,function(field,index){
			if (options.exclude.indexOf(field.key)!=-1)
				fields.splice(index,1);
		});
	}

	$scope.alterFields = function(fields){
		angular.forEach(fields,function(field,index){
			if (!field.validators)
				field.validators = {};
			var error_key = field.key;
			if (field.data)
				error_key = field.data.error_key ? field.data.error_key : field.key;
//			console.log('alterFields',field);
			field.validators['server'] = {
					expression: function(viewValue, modelValue, scope) {
//						console.log('expression',field.key,viewValue,modelValue,error_key,$scope.errors);
						if (!$scope.errors)
							return true;
						if (error_key.indexOf('data.')==0){
							if (!$scope.errors['data'])
								return true;
							return $scope.errors['data'][error_key.substr(5)] == null;
						}
//						console.log('error key',error_key,$scope.errors[error_key] == null,$scope.errors[error_key]);
						return $scope.errors[error_key] == null;
					},
					message: function()
					{	
//						console.log('message',field.key,error_key.substr(5));
						if (!$scope.errors)
							return;
						if (error_key.indexOf('data.')==0){
							if (!$scope.errors['data'])
								return;
							return $scope.errors['data'][error_key.substr(5)].join(', ');
						}
						if ($scope.errors[error_key])
							return $scope.errors[error_key].join(', ');
					}
			};
		});
		return fields;
	}
	$scope.fields = $scope.alterFields(fields);
	$scope.original_fields = $scope.fields;
	$scope.validateForm = function(){
//		console.log('validateForm',$scope.fields,$scope.errors);
		angular.forEach($scope.fields,function(field,index){
//			console.log('validate field',field);
			if (field.formControl){
				field.formControl.$validate();
				field.formControl.$setTouched(); //necessary to show message
			}
		});
	}
	$scope.onSubmit = function() {
//		console.log('save model',$scope.model)
		var method = $scope.model.id ? '$save' : '$create';
		$scope.model[method](
				function(){
//					$scope.errors = null;
//					$scope.validateForm();
					$modalInstance.close($scope.model);
				},
				function(response){
					$scope.errors = response.data;
					$scope.validateForm();
				}
		);
	}
	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};
}
)
.controller('ExtendedFormlyModalController', function FormlyModalController($scope,$controller, $http, $modalInstance,ModelType,ModelSubType,FormlyDynamicFields, fields, model, options) {
	angular.extend(this, $controller('FormlyModalController', {$scope, $http, $modalInstance, fields, model, options}));
	if (!$scope.model.data)
		$scope.model.data = {};
	if (options.subtype){
		var subtype_field ={
			    "key": "subtype",
			    "type": "select",
			    "templateOptions": {
			      "label": "Subtype",
			      "ngOptions": "option as option.name for option in to.options track by option.id",
			      "options": [],
			      "valueProp": "id",
			      "labelProp": "name"
			    },
			    "expressionProperties": {
			    	"hide": "!to.options.length"
			    }
			};
		$scope.original_fields.unshift(subtype_field);
		$scope.fields = $scope.original_fields;
		if ($scope.model.data.type)
			ModelSubType.query({type:$scope.model.data.type.id},function(options){
				$scope.fields[1].templateOptions.options = options;
				$scope.fields[1].hide = !options.length;
				console.log('subtype_options',$scope.fields[1].templateOptions.options);
			});
		
		
	}
	if (options.model_type_query){
		var model_types = ModelType.query(options.model_type_query||{}).$promise.then(
			function(types){
				var type_field = {
					    "key": "type",
					    "type": "select",
					    "templateOptions": {
					      "label": "Type",
					      "ngOptions": "option as option.name for option in to.options track by option.id",
					      "options": types,
					      "valueProp": "id",
					      "labelProp": "name"
					    }
				    };
				if (options.subtype)
					type_field.templateOptions.onChange = function(model,two,scope){
						ModelSubType.query({type:model.id},function(options){
							scope.fields[1].templateOptions.options = options;
							scope.fields[1].hide = !options.length;
							console.log('subtype_options',scope.fields[1].templateOptions.options);
						});//[{id:model.id,name:model.name}];//
					};
				$scope.original_fields.unshift(type_field);
				$scope.fields = $scope.original_fields;//angular.copy($scope.original_fields);
			}
		);
	}
	
	$scope.fields = $scope.original_fields;//angular.copy($scope.original_fields);//angular.copy($scope.original_fields).push(type_field);
	
	function setExtraFields(extra_fields){
		
		var fields = $scope.original_fields;//angular.copy($scope.original_fields);
//		console.log('extra',$scope.alterFields(extra_fields));
		extra_fields = $scope.alterFields(extra_fields);
		$scope.fields = fields.concat(extra_fields);
	}
	
	$scope.$watch('model.type',function(newValue,oldValue){
//		console.log('model.type',newValue,oldValue);
		if (!newValue)
			return;
		if (angular.isNumber(newValue))
			$scope.model_type=ModelType.get({id:newValue});
		if (newValue.id)
			$scope.model_type=ModelType.get({id:newValue.id});
	});
	$scope.$watch('model_type',function(newValue,oldValue){
		if (newValue)
			newValue.$promise.then(function(data){
//				console.log(data.fields,FormlyDynamicFields.translateFields(data.fields));
				var fields = FormlyDynamicFields.translateFields(data.fields);
				setExtraFields(fields);
			});
	});
//	if (options.postInit)
//		options.postInit($scope);
}
);
