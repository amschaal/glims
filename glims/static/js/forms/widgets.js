(function() {

	angular.module('formly.widgets',['formly','ngMessages','formlyBootstrap', 'ui.bootstrap', 'ui.select', 'ngSanitize','checklist-model'])
	.run(runBlock)

	runBlock.$inject = [ 'formlyConfig','$http','$window' ];

	function runBlock(formlyConfig,$http,$window) {
		formlyConfig.extras.errorExistsAndShouldBeVisibleExpression = 'fc.$touched || form.$submitted';
		
		formlyConfig.setType({
	        name: 'ui-select-multiple',
	        extends: 'select',
	        template:'<ui-select multiple data-ng-model="model[options.key]" data-required="{[to.required]}" data-disabled="{[to.disabled]}" on-remove="to.updateSelect($item,$model)" on-select="to.updateSelect($item,$model)" theme="bootstrap">\
    			<ui-select-match placeholder="{[to.placeholder]}" >{[to.labelFunc($item,to)]}</ui-select-match>\
		        <ui-select-choices data-repeat="{[to.options]}">\
		          <div ng-bind-html="to.labelFunc(option,to) | highlight: $select.search"></div>\
		        </ui-select-choices>\
		      </ui-select><a ng-click="model[options.key]=null;">Clear</a>'
	      });
		formlyConfig.setType({
            name: 'multiSelect',
            extends: 'select',
            template: '<select multiple class="form-control" ng-model="model[options.key]" ng-options="{[to.ngOptions]}"></select>'
        });
		formlyConfig.setType({
	        name: 'ui-select-search',
	        extends: 'select',
	        defaultOptions:{
	        	validation:{show:false},
//	        	expressionProperties: {
//	        	      "validation.show": function ($viewValue,$modelValue,scope){
//	        	    	  console.log('validation.show',$viewValue,$modelValue,scope);
//	        	    	  return scope.options.validation.errorExistsandShouldBeVisible;
////	        	    	  return true;
//	        	      }
//        	    },
	        	templateOptions: {
                    ngOptions: 'option in to.options | filter: $select.search track by option[to.valueProp]',//option[to.valueProp] as option in to.options | filter: $select.search
                    searchParam: 'search',
                    optionsAttr: 'bs-options',
                    valueProp: 'id',
                    minSearchChar: 0,
                    labelFunc: function(item,to){return item ? item[to.labelProp] : '';},
                    placeholder: 'Search',
                    required: false,
                    options: [],
                    refresh: function(name,field){
                    	if (name.length < field.templateOptions.minSearchChar){
                    		field.templateOptions.options = [];
                    		return;
                    	}
                    	var queryParams = {};
                    	queryParams[field.templateOptions.searchParam] = name;
          			  return  $http.get(field.templateOptions.url,{params:queryParams}).then(function(response){
          				  field.templateOptions.options = response.data.results;
          			  });
                    },
                    refreshDelay: 0
                  }
	        },
//	        controller: function ($scope) {
//	        	alert('bingo');
//	        },
	        wrapper: ['validation','bootstrapLabel','bootstrapHasError'],
	        template: '<ui-select data-ng-model="model[options.key]" data-required="{[to.required]}" data-disabled="{[to.disabled]}" on-remove="to.updateSelect($item,$model)" on-select="to.updateSelect($item,$model)" theme="bootstrap">\
				        <ui-select-match placeholder="{[to.placeholder]}" >{[to.labelFunc($select.selected,to)]}</ui-select-match>\
				        <ui-select-choices data-repeat="{[to.ngOptions]}" refresh="to.refresh($select.search, options)" refresh-delay="{[to.refreshDelay]}">\
				          <div ng-bind-html="to.labelFunc(option,to) | highlight: $select.search"></div>\
				        </ui-select-choices>\
				      </ui-select><a ng-click="model[options.key]=null;">Clear</a>'
	      });
		
		
		formlyConfig.setType({
	        name: 'ui-select-search-multiple',
	        extends: 'select',
	        defaultOptions:{
	        	validation:{show:false},
//	        	expressionProperties: {
//	        	      "validation.show": function ($viewValue,$modelValue,scope){
//	        	    	  console.log('validation.show',$viewValue,$modelValue,scope);
//	        	    	  return scope.options.validation.errorExistsandShouldBeVisible;
////	        	    	  return true;
//	        	      }
//        	    },
	        	templateOptions: {
                    ngOptions: 'option in to.options | filter: $select.search track by option[to.valueProp]',//option[to.valueProp] as option in to.options | filter: $select.search
                    searchParam: 'search',
                    optionsAttr: 'bs-options',
                    valueProp: 'id',
                    minSearchChar: 0,
                    labelFunc: function(item,to){return item ? item[to.labelProp] : '';},
                    placeholder: 'Search',
                    required: false,
                    options: [],
//                    url: '/api/get/url',
                    refresh: function(name,field){
                    	if (name.length < field.templateOptions.minSearchChar){
                    		field.templateOptions.options = [];
                    		return;
                    	}
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
	        template: '<ui-select multiple data-ng-model="model[options.key]" data-required="{[to.required]}" data-disabled="{[to.disabled]}" on-remove="to.updateSelect($item,$model)" on-select="to.updateSelect($item,$model)" theme="bootstrap">\
	        			<ui-select-match placeholder="{[to.placeholder]}" >{[to.labelFunc($item,to)]}</ui-select-match>\
				        <ui-select-choices data-repeat="{[to.ngOptions]}" refresh="to.refresh($select.search, options)" refresh-delay="{[to.refreshDelay]}">\
				          <div ng-bind-html="to.labelFunc(option,to) | highlight: $select.search"></div>\
				        </ui-select-choices>\
				      </ui-select><a ng-click="model[options.key]=null;">Clear</a>'
	      });
		
		
		formlyConfig.setType({
	        name: 'objectMultiCheckbox',
//	        extends: 'multiCheckbox',
	        template: '<div class="radio-group">\
					        	  <div ng-repeat="(key, option) in checkbox_options" class="checkbox">\
					        <label>\
					          <input type="checkbox"\
	        							data-checklist-model="model[options.key]"\
	        							data-checklist-value="option"\
	        							checklist-comparator=".id">\
	        							{[option[to.labelProp || \'name\']]}\
					        </label>\
					      </div>\
					    </div>',
	        wrapper: ['bootstrapLabel', 'bootstrapHasError'],
	        defaultOptions:{
	        	templateOptions: {
	        		'valueProp': 'id'
	        	}
	        },
	        controller: /* @ngInject */["$scope", function controller($scope) {
	        	$scope.checkbox_options = angular.copy($scope.to.options);
	        	//If the options change, remove invalid options from selection
		        $scope.$watch('to.options', function(options,oldOptions) {
		        	console.log('checkbox_options',options);
		        	if(!options.$promise || options.$resolved){
		        		$scope.checkbox_options = angular.copy(options);
		        		$scope.model[$scope.options.key] = _.intersectionWith(
		        				$scope.model[$scope.options.key], $scope.checkbox_options, 
			        			function(opt1,opt2){
			        				return opt1[$scope.to.valueProp]==opt2[$scope.to.valueProp];
			        			}
			        		);
		        	}
		        },true);
	        }]
	      });
		formlyConfig.setType({
	        name: 'subForm',
	        template: '{[model]}<formly-form model="sub_model" fields="to.form_fields" ></formly-form>',//'<h1>foo</h1>',
	        defaultOptions:{
	        	templateOptions: {
	        		'modelOptions': { allowInvalid: true },
	        		'form_fields': []
	        	}
	        },
	        controller: /* @ngInject */["$scope", function controller($scope) {
	        	//If the options change, remove invalid options from selection
	        	$scope.sub_model = $scope.model[$scope.options.key];
	        }]
	      });
		
	}

})();






//// File input type
//formlyConfig.setType({
//  name: 'upload',
//  extends: 'input',
//  wrapper: ['bootstrapLabel', 'bootstrapHasError'],
//  link: function(scope, el, attrs) {
//    el.on("change", function(changeEvent) {
//      var file = changeEvent.target.files[0];
//      if (file) {
//        var fileProp = {};
//        for (var properties in file) {
//          if (!angular.isFunction(file[properties])) {
//            fileProp[properties] = file[properties];
//          }
//        }
//        scope.fc.$setViewValue(fileProp);
//      } else {
//        scope.fc.$setViewValue(undefined);
//      }
//    });
//    el.on("focusout", function(focusoutEvent) {
//      // dont run validation , user still opening pop up file dialog
//      if ($window.document.activeElement.id === scope.id) {
//        // so we set it untouched
//        scope.$apply(function(scope) {
//          scope.fc.$setUntouched();  
//        });
//      } else {
//        // element losing focus so we trigger validation
//        scope.fc.$validate();
//      }
//    });
//    
//  },
//  defaultOptions: {
//    templateOptions: {
//      type: 'file',
//      required: true
//    }
//  }
//});
//
///* EXAMPLE 
//{
//    key: 'project_file',
//    type: 'upload',
//    templateOptions: {
//      label: 'test file upload'
//    }
//  },
//  */