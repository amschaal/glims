(function() {

	angular.module('formly.widgets',['formly','ngMessages','formlyBootstrap', 'ui.bootstrap', 'ui.select', 'ngSanitize'])
	.run(runBlock)

	runBlock.$inject = [ 'formlyConfig','$http' ];

	function runBlock(formlyConfig,$http) {
		formlyConfig.extras.errorExistsAndShouldBeVisibleExpression = 'fc.$touched || form.$submitted';
		formlyConfig.setType({
	        name: 'ui-select-multiple',
	        extends: 'select',
	        templateUrl: 'ui-select-multiple.html'
	      });
		formlyConfig.setType({
	        name: 'ui-select-multiple-search',
	        extends: 'select',
	        template: '<ui-select multiple data-ng-model="model[options.key]" data-required="{[to.required]}" data-disabled="{[to.disabled]}" theme="bootstrap">\
	            <ui-select-match placeholder="{[to.placeholder]}">{[to.labelFunc($item,to)]}</ui-select-match>\
	            <ui-select-choices data-repeat="{[to.ngOptions]}" data-refresh="to.refresh($select.search, options)" data-refresh-delay="{[to.refreshDelay]}">\
	              <div ng-bind-html="to.labelFunc(option,to) | highlight: $select.search"></div>\
	            </ui-select-choices>\
	          </ui-select>'
	      });
//		formlyConfig.setType({
//	        name: 'ui-select-multiple-search',
//	        extends: 'select',
//	        template: '<ui-select multiple data-ng-model="model[options.key]" data-required="{[to.required]}" data-disabled="{[to.disabled]}" theme="bootstrap">\
//	            <ui-select-match placeholder="{[to.placeholder]}">{[to.labelFunc($item,to)]}</ui-select-match>\
//	            <ui-select-choices data-repeat="{[to.ngOptions]}" data-refresh="to.refresh($select.search, options)" data-refresh-delay="{[to.refreshDelay]}">\
//	              <div ng-bind-html="to.labelFunc(option,to) | highlight: $select.search"></div>\
//	            </ui-select-choices>\
//	          </ui-select>'
//	      });
		formlyConfig.setType({
	        name: 'ui-select-search',
//	        extends: 'select',
	        defaultOptions:{
	        	templateOptions: {
                    ngOptions: 'option in to.options | filter: $select.search track by option[to.valueProp]',//option[to.valueProp] as option in to.options | filter: $select.search
                    searchParam: 'search',
                    optionsAttr: 'bs-options',
                    valueProp: 'id',
                    labelFunc: function(item,to){return item ? item[to.labelProp] : '';},
                    placeholder: 'Search',
                    options: [],
//                    url: '/api/get/url',
                    refresh: function(name,field){
//                    	console.log(name,field);
                    	var queryParams = {};
                    	queryParams[field.templateOptions.searchParam] = name;
//                    	return $http.get(field.templateOptions.url,queryParams);
          			  return  $http.get(field.templateOptions.url,queryParams).then(function(response){
//          				  console.log('results',response);
          				  field.templateOptions.options = response.data.results;
          			  });
                    },
                    refreshDelay: 0
                  }
	        },
//	        controller: function ($scope) {
//	        	alert('bingo');
//	        },
//	        template: '{[to]}',
	        wrapper: ['validation','bootstrapLabel','bootstrapHasError'],
	        template: '<ui-select data-ng-model="model[options.key]" data-required="{[to.required]}" data-disabled="{[to.disabled]}" theme="bootstrap">\
				        <ui-select-match placeholder="{[to.placeholder]}" data-allow-clear="true">{[to.labelFunc($select.selected,to)]}</ui-select-match>\
				        <ui-select-choices data-repeat="{[to.ngOptions]}" refresh="to.refresh($select.search, options)" refresh-delay="{[to.refreshDelay]}">\
				          <div ng-bind-html="to.labelFunc(option,to) | highlight: $select.search"></div>\
				        </ui-select-choices>\
				      </ui-select>'
//	        template: '<ui-select data-ng-model="model[options.key]" data-required="{[to.required]}" data-disabled="{[to.disabled]}" theme="bootstrap">\
//	            <ui-select-match placeholder="{[to.placeholder]}">{[to.labelFunc($item,to)]}</ui-select-match>\
//	            <ui-select-choices data-repeat="{[to.ngOptions]}" data-refresh="to.refresh($select.search, options)" data-refresh-delay="{[to.refreshDelay]}">\
//	              <div ng-bind-html="to.labelFunc(option,to) | highlight: $select.search"></div>\
//	            </ui-select-choices>\
//	          </ui-select>'
	      });
		formlyConfig.setType({
	        name: 'objectMultiCheckbox',
//	        extends: 'multiCheckbox',
	        template: '<div class="radio-group">\
					        	  <div ng-repeat="(key, option) in to.options" class="checkbox">\
					        <label>\
					          <input type="checkbox"\
					                 id="{[id + \'_\'+ $index]}"\
					                 ng-model="multiCheckbox.checked[$index]"\
					                 ng-change="multiCheckbox.change()">\
					          {[option[to.labelProp || \'name\']]}\
					        </label>\
					      </div>\
					    </div>',
	        wrapper: ['bootstrapLabel', 'bootstrapHasError'],
	        controller: /* @ngInject */["$scope", function controller($scope) {
	        	var to = $scope.to;
		        var opts = $scope.options;
		        $scope.multiCheckbox = {
		  	          checked: []
//		  	          change: setModel
		  	        };
		        function checkBoxes(selected,options){
		        	var ids = selected.map(function(obj){
		        		return obj[to.valueProp];
		        	});
		        	angular.forEach(options,function(option,index){
		        		$scope.multiCheckbox.checked[index] = ids.indexOf(option[to.valueProp]) !== -1;
		        	});
		        }
		        checkBoxes($scope.model[opts.key],to.options);
		        $scope.multiCheckbox.change = function() {
		        	console.log($scope.multiCheckbox.checked);
		        	var selected = [];
			          angular.forEach($scope.multiCheckbox.checked, function (checkbox, index) {
			            if (checkbox) {
			              selected.push(to.options[index]);
			            }
			          });
			          $scope.model[opts.key] = selected;
			          // Must make sure we mark as touched because only the last checkbox due to a bug in angular.
			          $scope.fc.$setTouched();
		        }
	        }]
	      });
	}

})();