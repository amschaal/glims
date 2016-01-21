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
	        templateUrl: 'ui-select-multiple-search.html'
	      });
		formlyConfig.setType({
	        name: 'objectMultiCheckbox',
//	        extends: 'multiCheckbox',
	        templateUrl: 'object-multi-checkbox.html',
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