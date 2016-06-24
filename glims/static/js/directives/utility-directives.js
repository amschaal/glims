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
}])
.directive('resourceFieldSelect', [function() {
    return {
        restrict: 'AE',
        replace: true,
        scope: {
        	resource: '=',
        	field: '@',
        	options: '=',
            optionId:'@',
            optionLabel: '@',
            onSuccess : '&?',
            onError : '&?'
        },
//        <select ng-change="setStatus(row)" ng-options="option.name for option in row.status_options track by option.id" ng-model="row.new_status" ng-init="row.new_status.id = row.status;"></select>
//    	<i class="fa fa-folder" ng-if="row.archived" title="Archived"></i>
//    	<button ng-show="row.new_status.id != row.status" ng-click="saveStatus(row)">Save</button>
        template: '<div>\
        			<select ng-options="status[optionId] as status[optionLabel] for status in options" ng-model="resource[field]" ng-change="save()"></select>\
		        	</div>',
        link: function($scope, iElement, iAttrs) {
        	var defaults = {
        			'onSuccess': function(){alert($scope.field+' updated');},
        			'onError': function(){alert('Error updating '+$scope.field);},
        			'optionId': 'id',
        			'optionLabel': 'name'
        	}
        	for (var field in defaults)
        		$scope[field] = angular.isDefined($scope[field]) ? $scope[field]: defaults[field];
        	$scope.save = function(){
        		$scope.resource.$save(null,$scope.onSuccess,$scope.onError);
        	}
        }
    };
}]);