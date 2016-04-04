
angular.module('mainapp')
.controller('FastaFileController', ['$scope', 'FastaFile','DRFNgTableParams', FastaFileController]);

function FastaFileController($scope,FastaFile,DRFNgTableParams) {
	$scope.headers=[{'name':'name','label':'Name'},{'name':'modified','label':'Last Modified'},{'name':'description','label':'Description'},{'name':'count','label':'Count'}];
	$scope.fastaLink = function(fasta_file){return django_js_utils.urls.resolve('proteomics__fasta_file', { pk: fasta_file.id })};
	$scope.fastaUpdateLink = function(fasta_file){return django_js_utils.urls.resolve('proteomics__update_fasta_file', { pk: fasta_file.id })};
	$scope.tableParams = DRFNgTableParams('/proteomics/api/fasta_files/',{sorting: { modified: "desc" }});
	$scope.deleteFile = function(file){
		file = new FastaFile(file);
		console.log($scope);
		console.log($scope.RemoteTableController);
		if(confirm('Are you sure you want to delete this file?')){
			file.$remove(function(){$scope.tableParams.reload();});
		}
	};
}

