angular.module("notifications", ["notifications.tpls","notifications.directives"]);
angular.module("notifications.tpls", ["template/notifications/subscription.html"]);
/*
 * <div remote-table headers="headers" url="/api/experiments/">
 *		<input ng-model="params.search" ng-change="load()" placeholder="Search"/>
 *		<table class="table table-striped table-condensed">
 *			<thead remote-headers></thead>
 *			<tr ng-repeat="row in rows">
 *	        <td>{[ row.name ]}</td>
 *	        <td>{[ row.description ]}</td>
 *	      </tr>
 *		</table>
 *		<div remote-pagination></div>
 *	</div> 
 *  
 */

angular.module('notifications.directives', ["notificationsModels"])
.directive('notificationSubscription', function(Subscription) {
	  return {
	    restrict: 'AE',
	    templateUrl: 'template/notifications/subscription.html',
	    scope: {
	    	objectId:'@',
	    	contentType:'@'
	    },
//	    link: function(scope,elem,attr){
//	    	console.log('scope',scope);
//	    	console.log('object_id',scope.objectId);
//	    	console.log('content_type',scope.contentType);
//	    	console.log('content_type__model',scope.contentTypeModel);
//	    }
	    controller: function($scope, $http, $element){
	    	this.$scope = $scope;
	    	$scope.subscription = Subscription.query({object_id:$scope.objectId,content_type:$scope.contentType},
	    			function(subscriptions){
	    				if (subscriptions.length > 1)
	    					throw 'A singular subscription object was not found';
	    				else if (subscriptions.length == 1)
	    					$scope.subscription = subscriptions[0];
	    				else
	    					$scope.subscription = new Subscription({object_id:$scope.objectId,content_type:$scope.contentType})
	    			},
	    			function(subscriptions){console.log('error',subscriptions);}
	    	);
	    	$scope.save = function(){
	    		if (!$scope.subscription.id)
	    			$scope.subscription.$create();
	    		else
	    			$scope.subscription.$save();
	    	}
	    	$scope.subscribe = function(){
	    		$scope.subscription.subscribed = true;
	    		$scope.subscription.email = true;
	    		$scope.save();
	    	}
	    	$scope.unsubscribe = function(){
	    		$scope.subscription.subscribed = false;
	    		$scope.subscription.email = false;
	    		$scope.save();
	    	}
	    }
	  }
	});


angular.module('template/notifications/subscription.html', []).run(['$templateCache', function($templateCache) {
	  $templateCache.put('template/notifications/subscription.html',
	'<div class="btn-group" uib-dropdown is-open="status.isopen">\
      <button id="single-button" type="button" class="btn btn-primary btn-sm">\
			  <span ng-if="subscription.subscribed" ng-click="unsubscribe()"><span class="glyphicon glyphicon-star" style="color:yellow" aria-hidden="true"></span> Unsubscribe</span>\
			  <span ng-if="!subscription.subscribed" ng-click="subscribe()">Subscribe</span>\
      </button>\
	  <button type="button" class="btn btn-primary btn-sm" uib-dropdown-toggle>\
        <span class="caret"></span>\
      </button>\
      <ul class="dropdown-menu" uib-dropdown-menu role="menu" aria-labelledby="single-button">\
        <li role="menuitem"><input type="checkbox" ng-model="subscription.email"/> Email</li>\
        <li class="divider"></li>\
        <li role="menuitem"><a href="#">Notifications</a></li>\
      </ul>\
    </div>'
	  );
	}]);

