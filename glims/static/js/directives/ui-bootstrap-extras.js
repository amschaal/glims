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
			model:'=?', //optional: set a model in the scope to the value returned by the modal
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

/*
.directive('modalSelect', function($compile,$uibModal,DRFNgTableParams) {
	return {
		restrict: 'A',
		scope: {
			modalTemplate:'@', //required: The $uibModalInstance template, passed as a string
			modalController:'@', //required: The $uibModalInstance controller, passed as a string
			setModel:'=?', //optional: set a model in the scope to the value returned by the modal
			onReturn:'=?', //optional: call this function on return, passing result 
			onCancel:'=?', //optional: call this function on cancel
			modalSize: '@?' //optional: modify size of modal,
			apiUrl: '@?',
			ngTableParams: '=?'
			
		},
	    link: function(scope, elm, attrs, ctrl)
	    {
	      scope.select = function(row){
    		  $uibModalInstance.close(row);
    	  }
	      scope.tableParams = DRFNgTableParams(scope.apiUrl,attrs.ngTableParams ? scope.ngTableParams : {});
	    }
	}
})
.controller('ParameterFileModalController', function FastaModalController($scope, $http,DRFNgTableParams, $uibModalInstance) {
  $scope
  $scope.tableParams = DRFNgTableParams('/proteomics/api/parameter_files/',{sorting: { modified: "desc" }});

}
);


angular.module("proteomics").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/proteomics/parameter_file_picker_modal.html',
	'	<div class="modal-header">\
            <h3 class="modal-title">Search Fasta Files</h3>\
            </div>\
            <div class="modal-body">\
    			 	<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed">\
    			      <tr ng-repeat="row in $data track by row.id">\
						<td data-title="\'Name\'" sortable="\'name\'"" filter="{name__icontains: \'text\'}">{[ row.name ]}</td>\
				        <td data-title="\'Type\'" sortable="\'type\'"" filter="{type__icontains: \'text\'}">{[ row.type ]}</td>\
				        <td data-title="\'Description\'" filter="{description__icontains: \'text\'}">{[row.description]}</td>\
    			        <td><a class="btn btn-xs btn-success" ng-hide="exists(row)" ng-click="select(row)">Select</a> </td>\
    			      </tr>\
    		    	</table>\
            </div>\
            <div class="modal-footer">\
              <!--  <button class="btn btn-warning" ng-click="save()">Save</button>-->\
            </div>'
	);
}]);
*/