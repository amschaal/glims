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
            onError : '&?',
            orderByField: '&?'
        },
//        <select ng-change="setStatus(row)" ng-options="option.name for option in row.status_options track by option.id" ng-model="row.new_status" ng-init="row.new_status.id = row.status;"></select>
//    	<i class="fa fa-folder" ng-if="row.archived" title="Archived"></i>
//    	<button ng-show="row.new_status.id != row.status" ng-click="saveStatus(row)">Save</button>
        template: '<div ng-show="options.length > 0">\
        				<select ng-options="status[optionId] as status[optionLabel] for status in options | orderBy:orderByField" ng-model="resource[field]" ng-change="save()"></select>\
		        	</div>',
        link: function($scope, iElement, iAttrs) {
        	var defaults = {
        			'onSuccess': function(){alert($scope.field+' updated');},
        			'onError': function(){alert('Error updating '+$scope.field);},
        			'optionId': 'id',
        			'optionLabel': 'name',
        			'orderByField': 'id'
        	}
        	for (var field in defaults)
        		$scope[field] = angular.isDefined($scope[field]) ? $scope[field]: defaults[field];
        	$scope.save = function(){
        		$scope.resource.$save(null,$scope.onSuccess,$scope.onError);
        	}
        }
    };
}])
.directive('remoteSelect', [function() {
	/*
		This makes it easy to create selects based on REST api.
		Usage: <remote-select url="/api/users/" model="project" field="manager"></remote-select>
		
		Notice that the 'field' parameter is required.  This is the field in the model that is being bound.
		For some reason it is difficult to get 2 way binding if using the field directly in ng-model.
	*/
	
    return {
        restrict: 'AE',
        replace: true,
        scope: {
            model: '=',  
            field: '@',  //field in model to be changed
            url:'@',  //api url
            config: '=' //optional settings
        },//required="settings.required" disabled="settings.disabled"//{[settings]}{[options]}
        template: '<div><ui-select data-ng-model="model[field]" on-remove="settings.onRemove($item,$model)" on-select="settings.onSelect($item,$model)" theme="bootstrap">\
			        <ui-select-match placeholder="{[settings.placeholder]}" >{[settings.labelFunc($select.selected)]}</ui-select-match>\
			        <ui-select-choices data-repeat="{[settings.ngOptions]}" refresh="settings.refresh($select.search)" refresh-delay="{[settings.refreshDelay]}">\
			          <div ng-bind-html="settings.labelFunc(option) | highlight: $select.search"></div>\
			        </ui-select-choices>\
			      </ui-select><a ng-click="model=null;">Clear</a></div>',
//        link: function(scope, iElement, iAttrs) {
//	    controllerAs: 'cx',
    	controller: function($scope, $http, $element){
    		console.log('config',$scope.config);
        	$scope.settings = {
        		required: false,
        		disabled: false,
        		onRemove: function($item,$model){},
        		onSelect: function($item,$model){},
        		placeholder: 'Search...',
    			valueProp: 'id',
    			labelProp: 'name',
    			ngOptions: 'option in options | filter: $select.search track by option[settings.valueProp]',
        		template: '<div>{[option[settings.labelProp]]}</div>',
	        	refresh: function(term) {
	        		console.log('refresh',term,$scope.url);
	        		
	        		return $http.get($scope.url, {params:{search: term}})
	        		.then(function(response) {
	        			$scope.options = response.data.results;
	        		});
	        	},
	        	labelFunc: function(option){
//	        		if ($scope.template)
//	        		return '<span ng-include="template"></span>';
	        		return option ? option[$scope.settings.labelProp] : '';
	        	},
        	};
        	angular.extend($scope.settings,$scope.config);
        	console.log('remoteSelect',$scope.settings);
        	$scope.options = [];
        }
    };
}]);