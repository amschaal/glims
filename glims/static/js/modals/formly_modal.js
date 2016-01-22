angular.module('formly.modal',[])
.config(function (formlyConfigProvider) {

    formlyConfigProvider.setWrapper({
      name: 'validation',
      types: ['input','textarea','select'],
      templateUrl: 'error-messages.html'
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
	      controller: 'FormlyModalController',
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
