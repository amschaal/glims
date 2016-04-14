angular.module("notifications", ["notifications.tpls","notifications.directives"]);
angular.module("notifications.tpls", ["template/notifications/subscription.html"]);

angular.module('notifications.directives', ["notificationsModels"])
.directive('notificationSubscription', function(Subscription,Notification) {
	  return {
	    restrict: 'AE',
	    templateUrl: 'template/notifications/subscription.html',
	    scope: {
	    	objectId:'@',
	    	contentType:'@'
	    },
	    controller: function($scope, $http, $element){
	    	this.$scope = $scope;
	    	$scope.subscription = Subscription.query({object_id:$scope.objectId,content_type:$scope.contentType},
	    			function(subscriptions){
	    				console.log('subscriptions',subscriptions);
	    				if (subscriptions.length > 1)
	    					throw 'A singular subscription object was not found';
	    				else if (subscriptions.length == 1)
	    					$scope.subscription = subscriptions[0];
	    				else
	    					$scope.subscription = new Subscription({object_id:$scope.objectId,content_type:$scope.contentType})
//	    				$scope.$watch('subscription.email',function(){
//	    					$scope.save();
//	    				});
	    			},
	    			function(subscriptions){console.log('error',subscriptions);}
	    	);
//	    	$scope.notifications = Notification.query({object_id:$scope.objectId,content_type:$scope.contentType});
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
	    	$scope.clear = function(){
	    		if ($scope.subscription.id)
	    			$scope.subscription.$clear();
	    	}
	    }
	  }
	});


angular.module('template/notifications/subscription.html', []).run(['$templateCache', function($templateCache) {
	  $templateCache.put('template/notifications/subscription.html',
	'<div class="btn-group" uib-dropdown is-open="status.isopen">\
	  <button id="single-button" type="button" class="btn btn-primary btn-sm" ng-if="!subscription.subscribed" ng-click="subscribe()">\
			  Subscribe\
      </button>\
	  <button id="single-button" type="button" class="btn btn-primary btn-sm" ng-if="subscription.subscribed" ng-click="unsubscribe()">\
			  <span class="glyphicon glyphicon-star" style="color:yellow" aria-hidden="true"></span> Unsubscribe <span ng-if="subscription.notifications.length">({[subscription.notifications.length]})</span>\
      </button>\
	  <button type="button" class="btn btn-primary btn-sm" uib-dropdown-toggle>\
        <span class="caret"></span>\
      </button>\
      <ul class="dropdown-menu dropdown-menu-right"  uib-dropdown-menu role="menu" aria-labelledby="single-button">\
        <!--<li role="menuitem"><input type="checkbox" ng-model="subscription.email"/> Email</li>\
        <li class="divider"></li>-->\
        <li ng-if="subscription.notifications.length" role="menuitem"><a ng-click="clear()"><i class="glyphicon glyphicon-remove"></i>Clear all</a></li>\
		<li ng-if="subscription.notifications.length" class="divider"></li>\
		<li ng-if="!subscription.notifications.length"><a>No notifications</a></li>\
		<li ng-repeat="n in subscription.notifications" class="notification notification-{[n.importance]}">\
			<a href="/notifications/{[n.id]}/" title="{[n.description]}"><span class="created">{[n.created | date: "short"]}</span> {[n.text]}</a>\
		</li>\
      </ul>\
    </div>'
	  );
	}]);

