angular.module('ui.bootstrap')
/*
Make use of $uibModal easier for common situations, such as assigning the result to a model in the controller scope.
IE: <button class="btn"  modal-launcher modal-controller="GroupModalController" modal-template="template/group_modal.html" set-model="group">Select group</button>
*/

.directive('modalLauncher', function($compile,$uibModal) {
	return {
		restrict: 'A',
		scope: {
			modalTemplate:'@', //required: The $uibModalInstance template, passed as a string
			modalController:'@', //required: The $uibModalInstance controller, passed as a string
			setModel:'=?', //optional: set a model in the scope to the value returned by the modal
			model:'=?', //optional: allow the modal to manipulate the model during execution
			onReturn:'=?', //optional: call this function on return, passing result 
			onCancel:'=?', //optional: call this function on cancel
			modalSize: '@?' //optional: modify size of modal
		},
	    link: function(scope, elm, attrs, ctrl)
	    {
	    	scope.openModal = function () {
			    var modalInstance = $uibModal.open({
			      templateUrl: scope.modalTemplate,
			      controller: scope.modalController,
			      size: attrs.size ? scope.size : 'lg',
	    		  resolve: {
	    		      model: function () {
	    		          return scope.model;
	    		      }
	    	      }
			    });

			    modalInstance.result.then(function (result) {
				    if (attrs.setModel)
				    	scope.setModel = result;
				    if (scope.onReturn)
				    	scope.onReturn(result);
			    }, function () {
			    	if (scope.onCancel)
			    	  scope.onCancel();
			    });
			  };
	      elm.attr("ng-click", "openModal()");
	      elm.removeAttr("modal-launcher");
	      $compile(elm)(scope);
	    }
	}
})
.directive('modalSelect', function($compile,$uibModal) {
	return {
		restrict: 'A',
		scope: {
			modalTemplate:'@', //required: The $uibModalInstance template, passed as a string
//			modalController:'@', //required: The $uibModalInstance controller, passed as a string
			setModel:'=?', //optional: set a model in the scope to the value returned by the modal
			model:'=?', //optional: allow the modal to manipulate the model during execution
			onReturn:'=?', //optional: call this function on return, passing result 
			onCancel:'=?', //optional: call this function on cancel
			modalSize: '@?', //optional: modify size of modal
			tableParams: '=',
			title:'@',
			multi:'@'
		},
//		controller: function ($scope, $element, $attrs) {
//		//  $scope.tableParams = DRFNgTableParams('/proteomics/api/parameter_files/',{sorting: { modified: "desc" }});
//			$scope.foo = 'bar';
//			$scope.select = function(row){
//				  $uibModalInstance.close(row);
//			  }
////	    	  $scope.tableParams = DRFNgTableParams('/proteomics/api/parameter_files/',{sorting: { modified: "desc" }});
//
//		},
	    link: function(scope, elm, attrs, ctrl)
	    {
	    	console.log('link',scope);
	    	console.log('attrs',attrs);
	    	scope.openModal = function () {
			    var modalInstance = $uibModal.open({
			      templateUrl: 'template/modals/select_modal.html',
			      controller: 'selectModalController',
			      size: attrs.size ? scope.size : 'lg',
	    		  resolve: {
	    		      setModel: function(){return scope.setModel},
	    		      tableParams: scope.tableParams,
	    		      template: function(){
	    		    	  return scope.modalTemplate;
	    		      },
	    		      options: function(){
	    		    	  return {title:scope.title,multi:attrs.multi==null?false:true,id:attrs.id?scope.id:'id'}
	    		      }
	    	      }
			    });

			    modalInstance.result.then(function (result) {
				    if (attrs.setModel)
				    	scope.setModel = result;
				    if (scope.onReturn)
				    	scope.onReturn(result);
			    }, function () {
			    	if (scope.onCancel)
			    	  scope.onCancel();
			    });
			  };
	      elm.attr("ng-click", "openModal()");
	      elm.removeAttr("modal-select");
	      $compile(elm)(scope);
	    }
	}
})
.directive('modalSelectActions', function() {  
  return {  
    template: '<a class="btn btn-xs btn-success" ng-click="select(row)" ng-if="!options.multi">Select</a><a class="btn btn-xs btn-success" ng-hide="isSelected(row)" ng-click="add(row)" ng-if="options.multi">Add</a><a class="btn btn-xs btn-danger" ng-show="isSelected(row)" ng-click="remove(row)" ng-if="options.multi">Remove</a>',  
    restrict: 'AE',  
  }  
})
.controller('selectModalController', function ($scope, $uibModalInstance,setModel,tableParams,template,options) {
	  $scope.value = angular.copy(setModel);
	  console.log('model',setModel,$scope.value);
	  $scope.tableParams = tableParams;
	  $scope.template = template;
	  $scope.options = options;
	  $scope.select = function(row){
		  $uibModalInstance.close(row);
	  }
	  $scope.save = function(){
		  $uibModalInstance.close($scope.value);
	  }
	  $scope.cancel = function(){
		  $uibModalInstance.dismiss();
	  }
	  $scope.add = function(row){
		  if(!angular.isArray($scope.value))
			  $scope.value = [row];
		  else
			  $scope.value.push(row);
	  }
	  $scope.remove = function(row){
		  if(!angular.isArray($scope.value))
			  $scope.value=null;
		  else{
			  for(var i in $scope.value){
				  if ($scope.value[i][options.id] == row[options.id]){
					  $scope.value.splice(i,1);
					  return;
				  }
			  }
		  }
	  }
	  $scope.isSelected = function(row){
		  if(!angular.isArray($scope.value))
			  return false;
		  for(var i in $scope.value){
			  if ($scope.value[i][options.id] == row[options.id])
				  return true;
		  }
		  return false;
	  }
	  
	}
)
.run(['$templateCache', function($templateCache) {
		$templateCache.put('template/modals/select_modal.html',
		'	<div class="modal-header">\
	            <h3 class="modal-title">{[options.title]}</h3>\
	            </div>\
	            <div class="modal-body">\
							<ng-include src="template"></ng-include>\
	            </div>\
	            <div class="modal-footer">\
	              <button ng-if="options.multi" class="btn btn-success" ng-click="save()">Save</button><button class="btn btn-warning" ng-click="cancel()">Cancel</button>\
	            </div>'
		);
}])
