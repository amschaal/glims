angular.module('mainapp')
.config(function (formlyConfigProvider) {

    formlyConfigProvider.setWrapper({
      name: 'validation',
      types: ['input','textarea'],
      templateUrl: 'error-messages.html'
    });

  })
.controller('FormlyModalController', function FormlyModalController($scope, $http, formlyValidationMessages, $modalInstance, fields, model) {
	
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
	
	angular.forEach(fields,function(field,index){
		field.validators = {
		          DRF: {
		              expression: function(viewValue, modelValue) {
		            	  if (!$scope.errors)
		            	  	return true;
		            	  console.log('WTF????',$scope.errors[field.key] == null,viewValue,modelValue)
		            	  return $scope.errors[field.key] == null;
		              },
					  message: function(){console.log('get message',$scope.errors[field.key].join(', '));return $scope.errors[field.key].join(', ');}
//		                var value = modelValue || viewValue;
//		                return /(\d{1,3}\.){3}\d{1,3}/.test(value);
//		              ,message: '$viewValue + " is not a valid IP Address"'
		            }
		};
		
	});
	
	
	$scope.fields = fields;
	console.log(model);
	$scope.model = model;
	$scope.options = {};
	$scope.onSubmit = function() {
//	      alert(JSON.stringify($scope.model), null, 2);
	      $scope.model.$save(
	    		  function(){$modalInstance.close($scope.model);},
	    		  function(data){
	    			  $scope.errors = data.data;
//	    			  angular.forEach(data.data,function(errors,key){
//	    				  $scope.form.$setValidity(key,false);  
//	    			  });
	    		  }
	      );
	    }
	$scope.dismiss = function () {
	    $modalInstance.dismiss('cancel');
	};
}
);
