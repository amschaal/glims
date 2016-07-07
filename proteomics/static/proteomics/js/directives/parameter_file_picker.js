angular.module("proteomics",[]);

//angular.module('plugins').requires.push("proteomics");

angular.module("proteomics")

//This is a generic work in progress and will be moved into a utility library.
.directive('modalLauncher', function($compile,$modal) {
	return {
		restrict: 'A',
		scope: {
			onReturn:'&',
			modalTemplate:'@',
			modalController:'@'
		},
	    link: function(scope, elm, attrs, ctrl)
	    {
	    	scope.openModal = function () {
			    var modalInstance = $modal.open({
			      templateUrl: scope.modalTemplate,
			      controller: scope.modalController,
			      size: 'lg',
//			      resolve: {
//			    	  onReturn: function () {
//				          return scope.onReturn;
//				      },
////				      scope: function () {
////				          return scope.parameterFile;
////				      }
//			      }
			    });

			    modalInstance.result.then(function (result) {
			    	console.log('return',result,scope.onReturn);
				      scope.onReturn(result);
			    }, function () {
				      $log.info('Modal dismissed at: ' + new Date());
			    });
			  };
	      elm.attr("ng-click", "openModal()");
	      elm.removeAttr("modal-launcher");
	      $compile(elm)(scope);
	    }
	}
})
.directive('parameterFilePicker', function($compile,$modal) {
	return {
		restrict: 'A',
		scope: {
			parameterFile:'='
		},
	    link: function(scope, elm, attrs, ctrl)
	    {
	    	scope.openModal = function () {
			    var modalInstance = $modal.open({
			      templateUrl: 'template/proteomics/parameter_file_picker_modal.html',
			      controller: 'ParameterFileModalController',
			      size: 'lg',
			      resolve: {
//			    	  selectFunc: function () {
//				          return $scope.selectFasta;
//				      },
				      scope: function () {
				          return scope.parameterFile;
				      }
			      }
			    });

			    modalInstance.result.then(function (data) {
//				      $scope.sample_data[String(data.sample.id)] = data.data;
			    }, function () {
//				      $log.info('Modal dismissed at: ' + new Date());
			    });
			  };
	      elm.attr("ng-click", "openModal()");
	      elm.removeAttr("parameter-file-picker");
	      $compile(elm)(scope);
	    }
	}
})
.controller('ParameterFileModalController', function FastaModalController($scope, $http,DRFNgTableParams, $modalInstance) {
  $scope.select = function(row){
	  $modalInstance.close(row);
  }
	
  $scope.tableParams = DRFNgTableParams('/proteomics/api/parameter_files/',{sorting: { modified: "desc" }});

}
);

angular.module("proteomics").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/proteomics/parameter_file_picker.html',
	'<button ng-click="openModal()">Select parameter file</button>'
	);
}]);


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


