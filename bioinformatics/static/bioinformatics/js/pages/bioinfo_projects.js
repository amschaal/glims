
angular.module('mainapp')
.controller('BioinfoProjectsController', ['$scope', 'BioinfoProject','DRFNgTableParams', BioinfoProjectsController]);

function BioinfoProjectsController($scope,BioinfoProject,DRFNgTableParams) {
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab })};
	$scope.tableParams = DRFNgTableParams('/bioinformatics/api/bioinfo_projects/',{sorting: { name: "desc" }});
//	$scope.deleteFile = function(file){
//		file = new FastaFile(file);
//		console.log($scope);
//		console.log($scope.RemoteTableController);
//		if(confirm('Are you sure you want to delete this file?')){
//			file.$remove(function(){$scope.tableParams.reload();});
//		}
//	};
}

