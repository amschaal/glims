
angular.module('mainapp')
.controller('BioinfoProjectsController', ['$scope', 'BioinfoProject','BioinfoProjectService','User','DRFNgTableParams', BioinfoProjectsController]);

function BioinfoProjectsController($scope,BioinfoProject,BioinfoProjectService,User,DRFNgTableParams) {
	$scope.init = function(params){
		$scope.users = User.query({groups__id:params.group_id},function(users){
			angular.forEach(users,function(user){
				user.title = user.first_name + ' ' + user.last_name;
			})
			users.unshift({id:null,title:''});
//			console.log(data,blah);
//			data.title = data.first_name + ' ' + data.last_name;
		});
	};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab })};
	$scope.tableParams = DRFNgTableParams('/bioinformatics/api/bioinfo_projects/',{sorting: { created: "desc" }});
//	$scope.deleteFile = function(file){
//		file = new FastaFile(file);
//		console.log($scope);
//		console.log($scope.RemoteTableController);
//		if(confirm('Are you sure you want to delete this file?')){
//			file.$remove(function(){$scope.tableParams.reload();});
//		}
//	};
	$scope.createProject = function(){
		BioinfoProjectService.create();
	}
}

