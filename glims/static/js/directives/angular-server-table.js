angular.module("remoteTable", ["remoteTable.tpls", "remoteTableDirectives"]);
angular.module("remoteTable.tpls", ["template/table/paginate.html", "template/table/headers.html"]);
/*
 * <div remote-table headers="headers" url="/api/experiments/">
 *		<input ng-model="params.search" ng-change="load()" placeholder="Search"/>
 *		<table class="table table-striped table-condensed">
 *			<thead remote-headers></thead>
 *			<tr ng-repeat="row in rows">
 *	        <td>{[ row.name ]}</td>
 *	        <td>{[ row.description ]}</td>
 *	      </tr>
 *		</table>
 *		<div remote-pagination></div>
 *	</div> 
 *  
 */

angular.module('remoteTableDirectives', [])
.directive('remoteTable', function() {
	  return {
	    restrict: 'AE',
	    scope: {headers:'=headers',url:'@url'},
	    /* transclude and link function necessary to ensure that the isolated scope is used by the enclosed markup */
	    transclude: true,
	    link: function(scope, element, attrs, ctrl, transclude) {
	        transclude(scope, function(clone) {
	         element.append(clone);
	        });
	      },
	    controller: function($scope, $http, $element){
	    	this.$scope = $scope;
	    	  
	      	$scope.rows=[];
	    	$scope.params={}
	    	$scope.settings = {'page_size':2,'page':1};
	    	$scope.parameter_map={'order_by':'ordering','page':'page','page_size':'page_size'};
	    	$scope.load = function () {
	    	  for (k in $scope.parameter_map){
	    		  if ($scope.settings[k])
	    			  $scope.params[$scope.parameter_map[k]]=$scope.settings[k];
	    	  }
	    	  $http.get($scope.url,{'params':$scope.params}).then(
	    			  function (response) {
	    				  $scope.count = response.data.count;
	    				  if ($scope.settings.page_size){
	    					  $scope.settings.pages = Math.ceil($scope.count / $scope.settings.page_size)
	    				  }
	    				  $scope.rows = response.data.results;
	    			  }
	    	  );
	    	};
	    	
	      $scope.initTable = function () {
	        $scope.load();
	      };
	      $scope.initTable();
	    }
	  }
	})
	.directive('remotePagination', function() {
	  return {
	    restrict: 'A',
	    require: '^remoteTable',
	    templateUrl: 'template/table/paginate.html',
	    replace: true,
	    link: function ($scope, element, attrs, remoteTable) {
	    	$scope.Range = function(start, end) {
	    	    var result = [];
	    	    for (var i = start; i <= end; i++) {
	    	        result.push(i);
	    	    }
	    	    return result;
	    	};
	    	$scope.setPageSize = function(size){
	    		remoteTable.$scope.settings.page_size=size;
	    		$scope.goToPage(1);
	    	};
	    	$scope.goToPage = function (page){
	    		remoteTable.$scope.settings.page = page;
	    		remoteTable.$scope.settings.page = page;
	    		remoteTable.$scope.load();
	    	};
	    	$scope.next = function(){
	    		if (remoteTable.$scope.settings.page < remoteTable.$scope.settings.pages){
	    			$scope.goToPage(remoteTable.$scope.settings.page + 1)
	    		}
	    	}
	    	$scope.prev = function(){
	    		if (remoteTable.$scope.settings.page > 1){
	    			$scope.goToPage(remoteTable.$scope.settings.page - 1)
	    		}
	    	}
	    }
	   }
	})
	.directive('remoteHeaders', function() {
	  return {
	    restrict: 'A',
	    require: '^remoteTable',
	    templateUrl: 'template/table/headers.html',
	    replace: true,
	    link: function ($scope, element, attrs, remoteTable) {
	    	$scope.orderBy = function(header){
	    		if (remoteTable.$scope.settings.order_by == header.name)
	    			remoteTable.$scope.settings.order_by = '-' + header.name;
	    		else
	    			remoteTable.$scope.settings.order_by = header.name;
	    		remoteTable.$scope.load();
	    	};
	    }
	   }
	});


angular.module('template/table/headers.html', []).run(['$templateCache', function($templateCache) {
	  $templateCache.put('template/table/headers.html',
	"<thead><tr><th ng-repeat=\"header in headers\" ng-click=\"orderBy(header)\">{[header.label]} <i ng-if=\"settings.order_by==header.name || settings.order_by=='-'+header.name\" class=\"glyphicon\" ng-class=\"{'glyphicon-sort-by-attributes': header.name == settings.order_by, 'glyphicon-sort-by-attributes-alt': '-'+header.name == settings.order_by}\"></i></th></tr></thead>"
	  );
	}]);

angular.module('template/table/paginate.html', []).run(['$templateCache', function($templateCache) {
	  $templateCache.put('template/table/paginate.html',
			  "<div class=\"row\"> \
			  <div class=\"col-sm-9\"> \
			  	<nav> \
			  	  <ul class=\"pagination\" ng-if=\"settings.pages\"> \
			  	    <li><a ng-click=\"prev()\">&laquo;</a></li> \
			  	    <li ng-repeat=\"p in Range(1,settings.pages)\" ng-class=\"{active: p == settings.page}\"><a ng-click=\"goToPage(p)\">{[p]}</a></li> \
			  	    <li><a ng-click=\"next()\">&raquo;</a></li> \
			  	  </ul> \
			  	</nav> \
			  </div> \
			  	 \
			  <div class=\"col-sm-3\"> \
			  	<div class=\"btn-group\"> \
			  	  <div type=\"button\" ng-repeat=\"size in [2,5,10,25]\" class=\"btn btn-default\" ng-click=\"setPageSize(size)\" ng-class=\"{active: size == settings.page_size}\">{[size]}</div> \
			  	</div> \
			  </div> \
			  </div>"
	   );
	}]);
