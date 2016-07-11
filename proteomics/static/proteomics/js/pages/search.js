
angular.module('mainapp').requires.push('proteomicsSelectModals');
angular.module('mainapp')
.controller('SearchController', ['$scope','$http','ParameterFile','$modal','$filter','proteomicsSelectModalService','selectModalService',SearchController]);

function SearchController($scope,$http,ParameterFile,$modal,$filter,proteomicsSelectModalService,selectModalService) {
	$scope.errors={};
	$scope.data={"engine":{"msgf":1,"omssa":1,"xtandem":1,"ms_amanda":1,"myrimatch":1,"comet":1,"tide":1},"samples":[],"fastas":[]};
	$scope.jobLink = function(job_id){return django_js_utils.urls.resolve('job', { id: job_id })};
	$scope.jobs = [];
	$scope.message = false;
	$scope.parameter_files = ParameterFile.query()
	$scope.init = function(){
	}
	$scope.getErrors = function(name){
		return $scope.errors[name] ? $scope.errors[name] : []; 
	};
	$scope.submit = function(){
		var url = django_js_utils.urls.resolve('proteomics__run_searchcli', {});
		//angular.merge({},...);
		var data = {'engine':$scope.data.engine,'threads':$scope.data.threads,'samples':[],'parameter_file':$scope.data.parameter_file};
		angular.forEach($scope.data.samples,function(sample,key){
			data['samples'].push(sample.id);
		});
		if ($scope.data.fastas[0])
			data['fasta_file'] = $scope.data.fastas[0].id;
		$http.post(
			url,
			data
		).success(function(data, status, headers, config) {
			if (data.errors){
				$scope.errors=data.errors;
				$scope.message = false;
			}
			else{
				if (data['URL'])
					window.location.href = data['URL'];
				$scope.errors = {}
				var time = $filter('date')(new Date(), 'HH:mm::ss');
				$scope.jobs.push({job_id:data['job_id'],job_date:new Date()});
			}
				
		});
	}
	  $scope.selectSamples = function(){
		  selectModalService.selectSamples({multi:true,initial:$scope.data.samples}).result.then(function(samples){$scope.data.samples=samples});
	  }
	  $scope.selectDefaultFile = function(){
		  proteomicsSelectModalService.selectDefaultFile({initial:$scope.parameter_file}).result.then(function(parameter_file){$scope.parameter_file=parameter_file});
	  }
	  $scope.selectFastaFile = function(){
		  proteomicsSelectModalService.selectFastaFile({initial:$scope.fasta}).result.then(function(fasta){$scope.fasta=fasta});
	  }
}



