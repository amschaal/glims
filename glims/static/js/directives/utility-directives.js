//Inspired by https://github.com/BhattaRj/angular-show-more

angular.module('utility.directives', [])
.directive('showMore', [function() {
    return {
        restrict: 'AE',
        replace: true,
        scope: {
            text: '=',
            limit:'=',
            lines: '=?',
            delimiter: '=?'
        },

        template: '<div class="show-more">\
		        		<span ng-if="show_all||!limited">{[text]} <a href="#" ng-click="less()" ng-if="limited">less</a></span>\
		        		<span ng-if="!show_all&&limited">{[shortened]} <a href="#" ng-click="more()">...more</a></span>\
		        	</div>',
        link: function(scope, iElement, iAttrs) {
        	scope.text = scope.text ? scope.text : '';
        	scope.limited = false;
        	scope.show_all = false;
        	scope.more = function(){
        		scope.show_all=true;
        	}
        	scope.less = function(){
        		scope.show_all=false;
        	}
            scope.formatText = function(text){
            	if (scope.lines && scope.delimiter){
            		var lines = text.split(scope.delimiter);
            		text = lines.splice(0,scope.lines).join(scope.delimiter);
            	}
            	return text.substr(0,scope.limit);
            };
            scope.shortened = scope.formatText(scope.text);
            if (scope.text.length > scope.shortened.length) {
                scope.limited = true;
            };
        }
    };
}]);