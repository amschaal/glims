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
			title:'@'
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
	    	scope.openModal = function () {
			    var modalInstance = $uibModal.open({
			      templateUrl: 'template/modals/select_modal.html',
			      controller: 'selectModalController',
			      size: attrs.size ? scope.size : 'lg',
	    		  resolve: {
	    		      model: scope.model,
	    		      tableParams: scope.tableParams,
	    		      template: function(){
	    		    	  return scope.modalTemplate;
	    		      },
	    		      options: function(){
	    		    	  return {title:scope.title}
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
    template: '<a class="btn btn-xs btn-success" ng-hide="exists(row)" ng-click="select(row)">Select</a>',  
    restrict: 'AE',  
  }  
})
.controller('selectModalController', function ($scope, $uibModalInstance,model,tableParams,template,options) {
	  $scope.select = function(row){
		  $uibModalInstance.close(row);
	  }
	  $scope.tableParams = tableParams;
	  $scope.template = template;
	  $scope.options = options;
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
	              <!--  <button class="btn btn-warning" ng-click="save()">Save</button>-->\
	            </div>'
		);
}])
