angular.module('proteomicsSelectModals',['selectModals'])
.service('proteomicsSelectModalService', function(SelectModalService,DRFNgTableParams) {
	 return {
		 selectFastaFile: selectFastaFile,
		 selectDefaultFile: selectDefaultFile
	 };
	  function selectFastaFile(options){ 
		  var defaultOptions = {
				  title: 'Search Fasta Files',
				  tableParams: DRFNgTableParams('/proteomics/api/fasta_files/',{sorting: { modified: "desc" }}),
				  template: 'proteomics/select_modals/fasta_modal.html'
		  }
		  angular.extend(defaultOptions,options?options:{});
		  return SelectModalService.openSelectModal(defaultOptions.template,defaultOptions.tableParams,defaultOptions);
	  }
	  function selectDefaultFile(options){ 
		  var defaultOptions = {
				  title: 'Search Default Files',
				  tableParams: DRFNgTableParams('/proteomics/api/parameter_files/',{sorting: { modified: "desc" }}),
				  template: 'proteomics/select_modals/parameter_modal.html'
		  }
		  angular.extend(defaultOptions,options?options:{});
		  return SelectModalService.openSelectModal(defaultOptions.template,defaultOptions.tableParams,defaultOptions);
	  }
	  
})
.run(['$templateCache', function($templateCache) {
		$templateCache.put('proteomics/select_modals/parameter_modal.html',
				'<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed"><tr ng-repeat="row in $data track by row.id"><td data-title="\'Name\'" sortable="\'name\'"" filter="{name__icontains: \'text\'}">{[ row.name ]}</td><td data-title="\'Type\'" sortable="\'type\'"" filter="{type__icontains: \'text\'}">{[ row.type ]}</td><td data-title="\'Description\'" filter="{description__icontains: \'text\'}">{[row.description]}</td><td modal-select-actions></td></tr></table>'
		);
}])
.run(['$templateCache', function($templateCache) {
		$templateCache.put('proteomics/select_modals/fasta_modal.html',
				'<table ng-table="tableParams" show-filter="true" class="table table-bordered table-striped table-condensed"><tr ng-repeat="row in $data track by row.id"><td data-title="\'Name\'" sortable="\'name\'"" filter="{name__icontains: \'text\'}">{[ row.name ]}</td><td data-title="\'Last Modified\'" sortable="\'modified\'">{[row.modified]}</td><td data-title="\'Description\'" filter="{description__icontains: \'text\'}">{[row.description]}</td><td data-title="\'Count\'" sortable="\'count\'">{[row.count]}</td><td modal-select-actions></td></tr></table>'
		);
}]);
