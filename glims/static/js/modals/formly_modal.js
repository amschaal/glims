angular.module('mainapp')
.config(function (formlyConfigProvider) {

    formlyConfigProvider.setWrapper({
      name: 'validation',
      types: ['input','textarea'],
      templateUrl: 'error-messages.html'
    });

  })
.controller('FormlyModalController', function FormlyModalController($scope, $http, formlyValidationMessages,formlyConfig, $modalInstance, fields, model) {
	formlyConfig.extras.errorExistsAndShouldBeVisibleExpression = 'fc.$touched || form.$submitted';

	formlyValidationMessages.addStringMessage('required', 'This field is required!');
//	
//	function getDRFMessage($viewValue, $modelValue, scope) {
//		return 'there was an error';
////		console.log($viewValue,$modelValue,scope);
//////	  if ($scope.errors.data.useGenericMessage) {
//////	    return 'This field is required';
//////	  } else {  
//////	    return scope.to.label + ' is required';
//////	  }
//	}
//	formlyValidationMessages.messages.DRF = getDRFMessage;
	
//	angular.forEach(fields,function(field,index){
//		field.validators = {
//		          DRF: {
//		              expression: function(viewValue, modelValue) {
//		            	  if (!$scope.errors)
//		            	  	return true;
//		            	  console.log('WTF????',$scope.errors[field.key] == null,viewValue,modelValue)
//		            	  return $scope.errors[field.key] == null;
//		              },
//					  message: function(){console.log('get message',$scope.errors[field.key].join(', '));return $scope.errors[field.key].join(', ');}
////		                var value = modelValue || viewValue;
////		                return /(\d{1,3}\.){3}\d{1,3}/.test(value);
////		              ,message: '$viewValue + " is not a valid IP Address"'
//		            }
//		};
//		
//	});
	
	   formlyConfig.extras.fieldTransform.push(fieldTransform);
	   function fieldTransform(fields, model) {
		      return fields.map(function(field) {
		    	  if (!field.validators)
		    		  field.validators = {};
		    	  field.validators['server'] = {
		    			  expression: function(viewValue, modelValue, scope) {
		    				  if (!$scope.errors)
			            	  	return true;
		    				  
			            	  console.log('WTF????',$scope.errors[field.key] == null,viewValue,modelValue)
			            	  return $scope.errors[field.key] == null;
			              },
						  message: function(){console.log('get message',$scope.errors[field.key].join(', '));return $scope.errors[field.key].join(', ');}
		    	  };
		        return field;
		      });
		    }
		        
	
	
	
	$scope.fields = fields;
	console.log(model);
	$scope.model = model;
	$scope.options = {};
	$scope.validateForm = function(){
		angular.forEach($scope.fields,function(field,index){
			field.formControl.$validate();
		});
	}
	$scope.onSubmit = function() {
	      $scope.model.$save(
	    		  function(){
//	    			  $scope.errors = null;
//	    			  $scope.validateForm();
	    			  $modalInstance.close($scope.model);
	    		  },
	    		  function(data){
	    			  $scope.errors = data.data;
	    			  $scope.validateForm();
	    		  }
	      );
	    }
	$scope.dismiss = function () {
	    $modalInstance.dismiss('cancel');
	};
}
);
