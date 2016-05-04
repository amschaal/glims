angular.module("plugins",[]);
angular.module("plugins").directive('bindUnsafeHtml', ['$compile', function ($compile) {
      return function(scope, element, attrs) {
          scope.$watch(
            function(scope) {
              // watch the 'bindUnsafeHtml' expression for changes
              return scope.$eval(attrs.bindUnsafeHtml);
            },
            function(value) {
              // when the 'bindUnsafeHtml' expression changes
              // assign it into the current DOM
              element.html(value);

              // compile the new DOM and link it to the current
              // scope.
              // NOTE: we only compile .childNodes so that
              // we don't get into infinite loop compiling ourselves
              $compile(element.contents())(scope);
            }
        );
    };
}])
.directive('objectPlugins', function() {
	return {
		restrict: 'AE',
		templateUrl: 'template/plugins/object-plugins.html',
//		scope: {
//			objectId:'@',
//			contentType:'@',
//		},
		scope: false,
		replace: true,
		controller: function ($scope,$rootScope,$http,$attrs) {
			$scope.object_id = $attrs['objectId'];
			$scope.content_type = $attrs['contentType'];
			console.log('plugin scope',$scope,$attrs);
			$http.get($rootScope.getURL('object_plugins',{content_type:$scope.content_type,pk:$scope.object_id}))
				.then(function(response){
					console.log('plugin data',response.data);
					$scope.plugins=response.data
				}
			);
		}
	}
});

angular.module("plugins").run(['$templateCache', function($templateCache) {
	$templateCache.put('template/plugins/object-plugins.html',
		'<tab ng-repeat="plugin in plugins">\
			<uib-tab-heading><span bind-unsafe-html="plugin.header"></span></uib-tab-heading>\
			<!--{[plugin.template]}-->\
			<div bind-unsafe-html="plugin.template"></div>\
		</tab>'
	);
}]);
