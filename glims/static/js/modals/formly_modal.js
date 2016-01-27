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
	    	  <!--{[model]}-->\
	      {[foo]}\
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
		          return angular.copy(model);
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
			default:
				return 'input';
		}
	}
	function translateField(field){
		return {
			    "key": "data."+field.name,
			    "type": translateFieldType(field.type),
			    "templateOptions": {
			      "label": field.label,
			      "required": field.required
				    }
				}
		
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

	$scope.alterFields = function(fields){
		angular.forEach(fields,function(field,index){
			if (!field.validators)
				field.validators = {};
			var error_key = field.key;
			if (field.data)
				error_key = field.data.error_key ? field.data.error_key : field.key;

			field.validators['server'] = {
					expression: function(viewValue, modelValue, scope) {
						if (!$scope.errors)
							return true;
						console.log('error key',error_key,$scope.errors[error_key] == null,$scope.errors[error_key]);
						return $scope.errors[error_key] == null;
					},
					message: function()
					{		
						if (!$scope.errors)
							return;
						console.log('get message',$scope.errors[error_key].join(', '));
						return $scope.errors[error_key].join(', ');
					}
			};
		});
		return fields;
	}
	$scope.original_fields = $scope.alterFields(fields);
	$scope.validateForm = function(){
		angular.forEach($scope.fields,function(field,index){
			field.formControl.$validate();
			field.formControl.$setTouched(); //necessary to show message
		});
	}
	$scope.onSubmit = function() {
		var method = $scope.model.id ? '$save' : '$create';
		$scope.model[method](
				function(){
//					$scope.errors = null;
//					$scope.validateForm();
					$modalInstance.close($scope.model);
				},
				function(data){
					$scope.errors = data.data;
					$scope.validateForm();
				}
		);
	}
	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};
}
)
.controller('ExtendedFormlyModalController', function FormlyModalController($scope,$controller, $http, $modalInstance,ModelType,FormlyDynamicFields, fields, model, options) {
	angular.extend(this, $controller('FormlyModalController', {$scope, $http, $modalInstance, fields, model, options}));
	
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
				$scope.original_fields.unshift(type_field);
				$scope.fields = angular.copy($scope.original_fields);
			}
		);
		
	}
	
	$scope.fields = angular.copy($scope.original_fields);//angular.copy($scope.original_fields).push(type_field);
	
	function setExtraFields(extra_fields){
		
		var fields = angular.copy($scope.original_fields);
		console.log('extra',$scope.alterFields(extra_fields));
		extra_fields = $scope.alterFields(extra_fields);
		$scope.fields = fields.concat(extra_fields);
	}
	
	$scope.$watch('model.type',function(newValue,oldValue){
		console.log('model.type',newValue,oldValue);
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
				console.log(data.fields,FormlyDynamicFields.translateFields(data.fields));
				var fields = FormlyDynamicFields.translateFields(data.fields);
				setExtraFields(fields);
			});
	});
//	$scope.model.type = 9; //test
}
);
