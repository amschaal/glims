
angular.module('mainapp')
.controller('BioinfoProjectController', ['$scope', 'BioinfoProject','User','DRFNgTableParams', BioinfoProjectController]);

function BioinfoProjectController($scope,BioinfoProject,User,DRFNgTableParams) {
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
	$scope.projectLink = function(project){return django_js_utils.urls.resolve('project', { pk: project.id })};
	$scope.labLink = function(project){return django_js_utils.urls.resolve('lab', { pk: project.lab })};
	$scope.options = {};	     	    
    $scope.fields = [
      {
        key: 'text',
        type: 'input',
        templateOptions: {
          label: 'Text',
          placeholder: 'Formly is terrific!'
        }
      },
      {
          key: 'description',
          type: 'textarea',
          templateOptions: {
            label: 'Description',
            placeholder: 'Enter stuff!'
          }
        }
    ];

    // function definition
    $scope.onSubmit = function() {
      alert(JSON.stringify($scope.model), null, 2);
    }
}

