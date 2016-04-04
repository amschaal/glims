angular.module('mainapp')
.controller('FastaModalController', function FastaModalController($scope, $http,DRFNgTableParams, $modalInstance,addFunc,scope) {
	$scope.addFunc = addFunc;
	$scope.scope = scope;
	$scope.headers=[{'name':'name','label':'Name'},{'name':'modified','label':'Last Modified'},{'name':'description','label':'Description'},{'name':'count','label':'Count'}];
	$scope.fastaLink = function(fasta_file){return django_js_utils.urls.resolve('proteomics__fasta_file', { pk: fasta_file.id })};
	$scope.exists = function(record){
		for (var i in $scope.scope){
			if ($scope.scope[i].id==record.id)
				return true;
		}
		return false;
	};
  $scope.dismiss = function () {
    $modalInstance.dismiss('cancel');
  };
	
  $scope.tableParams = DRFNgTableParams('/proteomics/api/fasta_files/',{sorting: { modified: "desc" }});

}
);
