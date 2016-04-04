
angular.module('mainapp')
.controller('UniprotController', ['$scope','$http', UniprotController]);

function UniprotController($scope,$http) {
	$scope.response={'headers':[],'rows':[]};
	$scope.params={limit:10};
	var csrf = $http.defaults.headers.common['X-CSRFToken'];
	$scope.search = function(){
		var params = {query:'organism:'+$scope.params.search,limit:$scope.params.limit,compress:'no',format:'tab'};
		delete $http.defaults.headers.common['X-CSRFToken'];
		$http({
			url:'http://www.uniprot.org/proteomes/',
			method: 'GET',
			params: params
		}).success(function(data, status, headers, config) {
			var rows = data.split('\n');
			$scope.response.headers = rows.shift().split('\t');
			$scope.response.rows = [];
			while(rows.length > 0){
				var row = rows.shift().split('\t');
				if (row.length > 1)
					$scope.response.rows.push(row);
			}
				
				
		});
	}
	$scope.preoteomeLink = function(row){
		return "http://www.uniprot.org/proteomes/" + row[0];
	}
	$scope.downloads = {};
	$scope.closeAlert = function(proteome) {
	    delete $scope.downloads[proteome];
	  };
	$scope.importProteome = function(row){
		console.log(row);
//		if ($scope.downloads[row[0]])
//			return;
		$scope.downloads[row[0]] = {row:row,message:'Downloading',status:'processing'};
		var url = django_js_utils.urls.resolve('proteomics__create_fasta_from_url');
		var params = {
				name:row[0],
				modified: row[2],
//				count: row[3],
				description:'Organism: '+row[1],//+' Modified: '+row[2]+' Protein Count: '+row[3],
				file_url: "http://www.uniprot.org/uniprot/?query=proteome:"+row[0]+"&force=true&format=fasta"
		};
		$http.defaults.headers.common['X-CSRFToken'] = csrf;
		$http.post(url,params)
		.success(function(data, status, headers, config) {
			$scope.downloads[row[0]].message = 'Import succeeded';
			$scope.downloads[row[0]].type = 'success';
		}).error(function(){
			$scope.downloads[row[0]].message = 'Failure importing proteome';
			$scope.downloads[row[0]].type = 'error';
		});
		
	};
	$scope.Utils = {
		     keys : Object.keys
		  };
}

