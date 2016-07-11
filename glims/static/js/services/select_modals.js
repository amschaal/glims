angular.module('selectModals',['ui.bootstrap', 'ngTable','utility.directives'])
.service('selectModalService', function($rootScope,$http,$uibModal,DRFNgTableParams) {
	 return {
		 openSelectModal: openSelectModal,
		 selectSamples: selectSamples
	 };
	 function openSelectModal (model,template,tableParams,options) { 
		 console.log('openSelectModal',model,template,tableParams,options)	;
		    var modalInstance = $uibModal.open({
			      templateUrl: 'template/select_modals/select_modal.html',
			      controller: options.controller ? options.controller : 'selectModalController',
			      size: options.size ? options.size : 'lg',
	    		  resolve: {
	    		      setModel: function(){return model},
	    		      tableParams: tableParams,
	    		      template: function(){
	    		    	  return template;
	    		      },
	    		      options: function(){
	    		    	  return {title:options.title,multi:options.multi?false:true,id:options.id?options.id:'id'}
	    		      }
	    	      }
			    });

			    modalInstance.result.then(function (result) {
			    	console.log(model,result);
//				    if (attrs.setModel)
				    	model = result;
				    if (options.onReturn)
				    	options.onReturn(result);
			    }, function () {
			    	if (options.onCancel)
			    	  options.onCancel();
			    });
			    return modalInstance;
	  }
	  function selectSamples(model,options){ 
		  var defaultOptions = {
				  title: 'Search Samples',
				  tableParams: DRFNgTableParams('/api/samples/',{sorting: { created: "desc" }}),
				  template: 'template/select_modals/sample_modal.html'
		  }
		  angular.extend(defaultOptions,options?options:{});
		  return openSelectModal(model,defaultOptions.template,defaultOptions.tableParams,defaultOptions);
	  } 
	  
})
.controller('selectModalController', function ($scope, $uibModalInstance,setModel,tableParams,template,options) {
	  $scope.value = angular.copy(setModel);
	  console.log('model',setModel,$scope.value);
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
.directive('modalSelectActions', function() {  
  return {  
    template: '<a class="btn btn-xs btn-success" ng-click="select(row)" ng-if="!options.multi">Select</a><a class="btn btn-xs btn-success" ng-hide="isSelected(row)" ng-click="add(row)" ng-if="options.multi">Add</a><a class="btn btn-xs btn-danger" ng-show="isSelected(row)" ng-click="remove(row)" ng-if="options.multi">Remove</a>',  
    restrict: 'AE',  
  }  
})
.run(['$templateCache', function($templateCache) {
		$templateCache.put('template/select_modals/select_modal.html',
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
	$templateCache.put('template/select_modals/sample_modal.html',
			'<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed"><tr ng-repeat="row in $data track by row.id"><td data-title="\'Created\'" sortable="\'created\'"">{[row.created|date]}</td><td data-title="\'ID\'" sortable="\'sample_id\'" filter="{sample_id__icontains: \'text\'}"><a target="_blank" href="{[ sampleLink(row) ]}">{[row.sample_id]}</a></td><td data-title="\'Name\'" sortable="\'name\'" filter="{name__icontains: \'text\'}">{[row.name]}</td><td data-title="\'Type\'" sortable="\'type__name\'" filter="{type__name__icontains: \'text\'}">{[row.type__name]}</td><td data-title="\'Project\'" sortable="\'project__name\'" filter="{project__name__icontains: \'text\'}"><a target="_blank" href="{[ projectLink(row) ]}">{[row.project__name]}</a></td><td data-title="\'Description\'" sortable="\'description\'" filter="{description__icontains: \'text\'}">{[row.description]}</td><td modal-select-actions></td></tr></table>'
	);
}]);
