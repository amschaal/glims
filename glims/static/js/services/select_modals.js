angular.module('selectModals',['ui.bootstrap', 'ngTable','utility.directives'])
.service('SelectModalService', function($uibModal,DRFNgTableParams) {
	console.log('got this far');
	 return {
		 openSelectModal: openSelectModal,
		 selectSamples: selectSamples,
		 selectLibraries: selectLibraries,
		 selectFiles: selectFiles
	 };
	 function openSelectModal (template,tableParams,options) { 
		 console.log('openSelectModal',template,tableParams,options)	;
		    var modalInstance = $uibModal.open({
			      templateUrl: 'glims/select_modals/select_modal.html',
			      controller: options.controller ? options.controller : 'selectModalController',
			      size: options.size ? options.size : 'lg',
	    		  resolve: {
	    		      initial: function(){return options.initial},
	    		      tableParams: tableParams,
	    		      template: function(){
	    		    	  return template;
	    		      },
	    		      options: function(){
	    		    	  return {title:options.title,multi:options.multi,id:options.id?options.id:'id'}
	    		      }
	    	      }
			    });
			    return modalInstance;
	  }
	  //example: selectModalService.selectSamples({multi:true,initial:$scope.samples}).result.then(function(samples){$scope.samples=samples});
	  function selectSamples(options){ 
		  var defaultOptions = {
				  title: 'Search Samples',
				  tableParams: DRFNgTableParams('/api/samples/',{sorting: { created: "desc" }}),
				  template: 'glims/select_modals/sample_modal.html'
		  }
		  angular.extend(defaultOptions,options?options:{});
		  return openSelectModal(defaultOptions.template,defaultOptions.tableParams,defaultOptions);
	  }
	  function selectLibraries(options){ 
		  var defaultOptions = {
				  title: 'Search Libraries',
				  tableParams: DRFNgTableParams('/api/libraries/',{sorting: { created: "desc" }}),
				  template: 'glims/select_modals/library_modal.html'
		  }
		  angular.extend(defaultOptions,options?options:{});
		  return openSelectModal(defaultOptions.template,defaultOptions.tableParams,defaultOptions);
	  }
	  function selectFiles(baseUrl,options){
		  var modalInstance = $uibModal.open({
		      templateUrl: options.template || 'glims/select_modals/select_files_modal.html',
		      controller: options.controller || 'selectFilesModalController',
		      size: options.size || 'lg',
    		  resolve: {
    		      baseUrl: function(){return baseUrl},
    		      options: function(){
    		    	  return options;
    		      }
    	      }
		    });
		    return modalInstance;
	  }
	  
})
.controller('selectModalController', function ($scope, $uibModalInstance,initial,tableParams,template,options) {
	  $scope.value = angular.copy(initial);
	  $scope.tableParams = tableParams;
	  $scope.template = template;
	  $scope.options = options;
	  $scope.select = function(row){
		  $uibModalInstance.close(row);
	  }
	  $scope.save = function(){
		  $uibModalInstance.close($scope.value);
	  }
	  $scope.cancel = function(){
		  $uibModalInstance.dismiss();
	  }
	  $scope.add = function(row){
		  if(!angular.isArray($scope.value))
			  $scope.value = [row];
		  else
			  $scope.value.push(row);
	  }
	  $scope.remove = function(row){
		  if(!angular.isArray($scope.value))
			  $scope.value=null;
		  else{
			  for(var i in $scope.value){
				  if ($scope.value[i][options.id] == row[options.id]){
					  $scope.value.splice(i,1);
					  return;
				  }
			  }
		  }
	  }
	  $scope.isSelected = function(row){
		  if(!angular.isArray($scope.value))
			  return false;
		  for(var i in $scope.value){
			  if ($scope.value[i][options.id] == row[options.id])
				  return true;
		  }
		  return false;
	  }
	  
	}
)
.controller('selectFilesModalController', function ($scope, $uibModalInstance,baseUrl,options) {
	  $scope.options = angular.copy(options);
	  $scope.selection = options.selection ? angular.copy(options.selection) : [];
	  $scope.actions = options.actions;
	  $scope.baseUrl = baseUrl;
	  $scope.done = function(){
		  var old_selection = options.selection || []
		  var added = _.difference($scope.selection,old_selection)
		  var removed = _.difference(old_selection,$scope.selection)
		  $uibModalInstance.close({'selection':$scope.selection,'added':added,'removed':removed});
	  }
	  $scope.cancel = function(){
		  $uibModalInstance.dismiss();
	  }
	}
)
.directive('modalSelectActions', function() {  
  return {  
    template: '<a class="btn btn-xs btn-success" ng-click="select(row)" ng-if="!options.multi">Select</a><a class="btn btn-xs btn-success" ng-hide="isSelected(row)" ng-click="add(row)" ng-if="options.multi">Add</a><a class="btn btn-xs btn-danger" ng-show="isSelected(row)" ng-click="remove(row)" ng-if="options.multi">Remove</a>',  
    restrict: 'AE',  
  }  
})
.run(['$templateCache', function($templateCache) {
		$templateCache.put('glims/select_modals/select_modal.html',
		'	<div class="modal-header">\
	            <h3 class="modal-title">{[options.title]}</h3>\
	            </div>\
	            <div class="modal-body">\
							<ng-include src="template"></ng-include>\
	            </div>\
	            <div class="modal-footer">\
	              <button ng-if="options.multi" class="btn btn-success" ng-click="save()">Save</button><button class="btn btn-warning" ng-click="cancel()">Cancel</button>\
	            </div>'
		);
}])

.run(['$templateCache', function($templateCache) {
	$templateCache.put('glims/select_modals/sample_modal.html',
			'<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed"><tr ng-repeat="row in $data track by row.id"><td data-title="\'Created\'" sortable="\'created\'"">{[row.created|date]}</td><td data-title="\'ID\'" sortable="\'sample_id\'" filter="{sample_id__icontains: \'text\'}"><a target="_blank" href="{[ sampleLink(row) ]}">{[row.sample_id]}</a></td><td data-title="\'Name\'" sortable="\'name\'" filter="{name__icontains: \'text\'}">{[row.name]}</td><td data-title="\'Type\'" sortable="\'type__name\'" filter="{type__name__icontains: \'text\'}">{[row.type.name]}</td><td data-title="\'Project\'" sortable="\'project__name\'" filter="{project__name__icontains: \'text\'}"><a target="_blank" href="{[ projectLink(row) ]}">{[row.project.name]}</a></td><td data-title="\'Description\'" sortable="\'description\'" filter="{description__icontains: \'text\'}">{[row.description]}</td><td modal-select-actions></td></tr></table>'
	);
}])
.run(['$templateCache', function($templateCache) {
	$templateCache.put('glims/select_modals/library_modal.html',
			'<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed"><tr ng-repeat="row in $data track by row.id"><td data-title="\'Created\'" sortable="\'created\'"">{[row.created|date]}</td><td data-title="\'ID\'" sortable="\'sample__sample_id\'" filter="{sample__sample_id__icontains: \'text\'}"><a target="_blank" href="{[ sampleLink(row) ]}">{[row.sample.sample_id]}</a></td><td data-title="\'Name\'" sortable="\'name\'" filter="{name__icontains: \'text\'}">{[row.name]}</td><td data-title="\'Type\'" sortable="\'type__name\'" filter="{type__name__icontains: \'text\'}">{[row.type.name]}</td><td data-title="\'Project\'" sortable="\'sample__project__name\'" filter="{sample__project__name__icontains: \'text\'}"><a target="_blank" href="{[ projectLink(row) ]}">{[row.sample.project.name]}</a></td><td data-title="\'Description\'" sortable="\'description\'" filter="{description__icontains: \'text\'}">{[row.description]}</td><td modal-select-actions></td></tr></table>'
	);
}])
.run(['$templateCache', function($templateCache) {
	$templateCache.put('glims/select_modals/select_files_modal.html',
	'	<div class="modal-header">\
            <h3 class="modal-title">{[options.title]}</h3>\
            </div>\
            <div class="modal-body">\
				<list-files base-url="{[baseUrl]}" selection="selection" actions="actions"></list-files>\
            </div>\
            <div class="modal-footer">\
              <button class="btn btn-success" ng-click="done()">Done</button><button class="btn btn-warning" ng-click="cancel()">Cancel</button>\
            </div>'
	);
}]);
