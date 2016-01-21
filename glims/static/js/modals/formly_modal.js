angular.module('formly.modal',[])
.config(function (formlyConfigProvider) {

    formlyConfigProvider.setWrapper({
      name: 'validation',
      types: ['input','textarea','select'],
      templateUrl: 'error-messages.html'
    });

  })
.controller('FormlyModalController', function FormlyModalController($scope, $http, $modalInstance, fields, model, options) {
	
	
	$scope.title = options.title ? options.title : 'Edit';

	   fields = angular.copy(fields);
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
	$scope.cancel = function () {
	    $modalInstance.dismiss('cancel');
	};
}
);
