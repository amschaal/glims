angular.module('tastyAngular',[])
	.directive("angularForm", ['$compile',function($compile) {
	  var linkFunction = function(scope, element, attributes) {
		  angular.forEach(element.children(),function(child,key){
			  var name = $(child).find('[name]').attr('name');
			  $(child).attr('ng-class',"{'has-error':getErrors('"+name+"').length}");
			  $(child).find('.controls').append('<p class="help-block" ng-repeat="error in getErrors(\''+name+'\')"><strong>{[error]}</strong></p>');
		  });
		  element.removeAttr('angular-form');
		  $compile(element)(scope);
	  };

	  return {
	    link: linkFunction,
	    replace: false,
	      terminal: true,
	      priority: 1000
	  };
	}]);
//.directive('initModel', function($compile) {
//    return {
//        restrict: 'A',
//        link: function(scope, element, attrs) {
//            scope[attrs.initModel] = element[0].value;
//            element.attr('ng-model', attrs.initModel);
//            element.removeAttr('init-model');
//            $compile(element)(scope);
//        }
//    };
//});