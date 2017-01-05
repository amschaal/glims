angular.module("accounts-plugin");

angular.module('plugins').requires.push("accounts-plugin");

angular.module("accounts-plugin")
.directive('projectAccounts', function(Account) {
	return {
		restrict: 'AE',
		templateUrl: 'template/accounts/accounts.html',
		scope: {
			projectId:'=',
			types:'='
		},
		controller: function ($scope,$rootScope) {
			$scope.accounts = [];
			function setAccountsCount(){
				$rootScope.accounts_count = $scope.accounts.length;
			}
			$scope.deleteAccount = function(index){
				if (!$scope.accounts[index].id)
					$scope.accounts.splice(index,1);
				else {
					if (!confirm("Are you sure you want to delete this account?"))
						return;
					$scope.accounts[index].$remove(function(){
						$scope.accounts.splice(index,1);
						setAccountsCount();
					});
				}
			};
			$scope.editAccount = function(account){
				account.editing = true;
			};
			$scope.save = function(account){
				if(account.id)
					account.$save(function(){},function(response){account.errors = response.data;});
				else
					account.$create(function(){setAccountsCount();},function(response){account.errors = response.data;});
			};
			$scope.newAccount = function(){
				var account = new Account({project:$scope.projectId});
				account.editing=true;
				$scope.accounts.push(account);
			};
			
			$scope.$watch('projectId',function(projectId,oldValue){
				if (!projectId)
					return;
				$scope.accounts = Account.query({project:projectId},function(){setAccountsCount()});
			});
			
		}
	}
});

angular.module("accounts-plugin").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/accounts/accounts.html',
	'<h4 ng-if="!accounts.length">There are currently no Accounts.</h4>\
	<table class="table" ng-if="accounts.length">\
	<tr class="no-border-top"><th>Type</th><th>Account</th><th>Description</th><td></td></tr>\
	<tr ng-repeat="account in accounts">\
	<td ng-if="!account.editing">{[types[account.type]]}</span></td>\
	<td ng-if="account.editing">\
			<p class="error" ng-repeat="error in account.errors.type">{[error]}</p>\
			<select ng-options="id as label for (id,label) in types" ng-model="account.type" class="form-control"></select>\
	</td>\
	<td ng-if="!account.editing">\
			<p class="error" ng-repeat="error in account.errors.account">{[error]}</p>\
			{[account.account]}\
	</td>\
	<td ng-if="account.editing"><input ng-model="account.account" class="form-control"/></td>\
	<td ng-if="!account.editing">{[account.description]}</td><td ng-if="account.editing"><textarea ng-model="account.description" class="form-control"></textarea></td>\
	<td>\
		<button class="btn btn-xs btn-danger pull-right" ng-click="deleteAccount($index)">Delete</button>\
		<button class="btn btn-xs pull-right" ng-if="!account.editing" ng-click="editAccount(account)">Edit</button>\
		<button class="btn btn-xs btn-success pull-right" ng-if="account.editing" ng-click="save(account)">Save</button>\
	</td>\
	</tr>\
	</table>\
	<button ng-click="newAccount()" class="btn btn-success">Add Account</button>'
	);
}]);


