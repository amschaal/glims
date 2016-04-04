var transformDjangoRestResponse = function(data, headers){
	try {
        var jsonObject = JSON.parse(data); // verify that json is valid
        return jsonObject.results;
    }
    catch (e) {
        console.log("did not receive a valid Json: " + e)
    }
    return {};
}

angular.module('glimsModels')
.factory('FastaFile', ['$resource', function ($resource) {
  return $resource('/proteomics/api/fasta_files/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' }
  });
}])
.factory('ParameterFile', ['$resource', function ($resource) {
  return $resource('/proteomics/api/parameter_files/:id/', {id:'@id'}, {
    query: { method: 'GET', transformResponse:transformDjangoRestResponse, isArray:true },
    save : { method : 'PUT' },
    create : { method : 'POST' },
    remove : { method : 'DELETE' }
  });
}]);

