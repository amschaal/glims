
angular.module('mainapp')
.controller('ParameterFileController', ['$scope', 'FastaFile','DRFNgTableParams', ParameterFileController]);

function ParameterFileController($scope,FastaFile,DRFNgTableParams) {
	$scope.parameterUpdateLink = function(parameter_file){return django_js_utils.urls.resolve('proteomics__update_parameter_file', { pk: parameter_file.id })};
	$scope.tableParams = DRFNgTableParams('/proteomics/api/parameter_files/',{sorting: { name: "desc" }});
	$scope.deleteFile = function(file){
		file = new FastaFile(file);
		console.log($scope);
		console.log($scope.RemoteTableController);
		if(confirm('Are you sure you want to delete this file?')){
			file.$remove(function(){$scope.tableParams.reload();});
		}
	};
}

