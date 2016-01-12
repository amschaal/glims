angular.module('mainapp')
.config(function (formlyConfigProvider) {

    formlyConfigProvider.setWrapper({
      name: 'validation',
      types: ['input','textarea','select'],
      templateUrl: 'error-messages.html'
    });

  })
.controller('FormlyModalController', function FormlyModalController($scope, $http, formlyValidationMessages,formlyConfig, $modalInstance, fields, model) {
	formlyConfig.extras.errorExistsAndShouldBeVisibleExpression = 'fc.$touched || form.$submitted';

//	formlyValidationMessages.addStringMessage('required', 'This field is required!');
//	formlyValidationMessages.messages.server= getServerMessage;
//
//	function getServerMessage($viewValue, $modelValue, scope) {
//		console.log('server message');
//		return 'wtf';
//	  if (scope.data.useGenericMessage) {
//	    return 'This field is required';
//	  } else {  
//	    return scope.to.label + ' is required';
//	  }
//	}
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
	   fields = angular.copy(fields);
//	   formlyConfig.extras.fieldTransform.push(fieldTransform);
//	   function fieldTransform(fields, model) {
//		      return fields.map(function(field) {
//		    	  if (!field.validators)
//		    		  field.validators = {};
//		    	  var error_key = field.key;
//		    	  if (field.data)
//		    		  error_key = field.data.error_key ? field.data.error_key : field.key;
//		    	  
//		    	  field.validators['server'] = {
//		    			  expression: function(viewValue, modelValue, scope) {
//		    				  console.log('error key',error_key,$scope.errors[error_key] == null,$scope.errors[error_key]);
//		    				  if (!$scope.errors)
//			            	  	return true;
//			            	  return $scope.errors[error_key] == null;
//			              },
//						  message: function()
//						  {		
//							  	console.log('get message',$scope.errors[error_key].join(', '));
//						  		return $scope.errors[error_key].join(', ');
//						  }
//		    	  };
//		        return field;
//		      });
//		    }
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
					  	console.log('get message',$scope.errors[error_key].join(', '));
				  		return $scope.errors[error_key].join(', ');
				  }
    	  };
   });
	
	
	
	$scope.fields = fields;
	console.log(model);
	$scope.model = model;
	$scope.options = {};
	$scope.validateForm = function(){
		angular.forEach($scope.fields,function(field,index){
			field.formControl.$validate();
			field.formControl.$setTouched(); //necessary to show message
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
