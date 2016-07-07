angular.module("proteomics",[]);

//angular.module('plugins').requires.push("proteomics");

angular.module("proteomics")
.directive('parameterFilePicker', function() {
	return {
		restrict: 'AE',
		templateUrl: 'template/proteomics/parameter_file_picker.html',
		scope: {
			parameterFile:'='
		},
		controller: function ($scope,$rootScope,$modal) {
			$scope.openModal = function () {
			    var modalInstance = $modal.open({
			      templateUrl: 'template/proteomics/parameter_file_picker_modal.html',
			      controller: 'ParameterFileModalController',
			      size: 'lg',
			      resolve: {
//			    	  selectFunc: function () {
//				          return $scope.selectFasta;
//				      },
				      scope: function () {
				          return $scope.parameterFile;
				      }
			      }
			    });

			    modalInstance.result.then(function (data) {
//				      $scope.sample_data[String(data.sample.id)] = data.data;
			    }, function () {
//				      $log.info('Modal dismissed at: ' + new Date());
			    });
			  };
		}
	}
})
.controller('ParameterFileModalController', function FastaModalController($scope, $http,DRFNgTableParams, $modalInstance,scope) {
	$scope.selectFunc = function(parameter_file){
		$scope.scope = parameter_file;
		$modalInstance.dismiss('cancel');
	}//selectFunc;
	$scope.scope = scope;
  $scope.dismiss = function () {
    $modalInstance.dismiss('cancel');
  };
	
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
    			        <td><a class="btn btn-xs btn-success" ng-hide="exists(row)" ng-click="selectFunc(row)">Select</a> </td>\
    			      </tr>\
    		    	</table>\
            </div>\
            <div class="modal-footer">\
                <button class="btn btn-warning" ng-click="dismiss()">Dismiss</button>\
            </div>'
	);
}]);


