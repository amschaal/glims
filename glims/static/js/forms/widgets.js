(function() {

	angular.module('formly.widgets',['formly','formlyBootstrap'])
	.run(runBlock)

	runBlock.$inject = [ 'formlyConfig' ];

	function runBlock(formlyConfig) {
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