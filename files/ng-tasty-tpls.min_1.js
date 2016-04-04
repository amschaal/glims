/*
 * ng-tasty
 * https://github.com/Zizzamia/ng-tasty

 * Version: 0.3.0 - 2014-10-22
 * License: MIT
 */
angular.module("ngTasty",["ngTasty.tpls","ngTasty.filter","ngTasty.service","ngTasty.table"]),angular.module("ngTasty.tpls",["template/table/head.html","template/table/pagination.html"]),angular.module("ngTasty.filter",["ngTasty.filter.cleanFieldName","ngTasty.filter.filterInt","ngTasty.filter.range"]),angular.module("ngTasty.filter.cleanFieldName",[]).filter("cleanFieldName",function(){return function(input){return input.replace(/[^a-zA-Z0-9-]+/g,"-")}}),angular.module("ngTasty.filter.filterInt",[]).filter("filterInt",function(){return function(input){return/^(\-|\+)?([0-9]+|Infinity)$/.test(input)?Number(input):0/0}}),angular.module("ngTasty.filter.range",[]).filter("range",["$filter",function($filter){return function(input,start,stop,step){if(start=$filter("filterInt")(start),stop=$filter("filterInt")(stop),step=$filter("filterInt")(step),isNaN(start)&&(start=0),isNaN(stop)&&(stop=start,start=0),isNaN(step)&&(step=1),step>0&&start>=stop||0>step&&stop>=start)return[];for(var i=start;step>0?stop>i:i>stop;i+=step)input.push(i);return input}}]),angular.module("ngTasty.service",["ngTasty.service.tastyUtil","ngTasty.service.debounce","ngTasty.service.setProperty","ngTasty.service.joinObjects"]),angular.module("ngTasty.service.tastyUtil",["ngTasty.service.debounce","ngTasty.service.setProperty","ngTasty.service.joinObjects"]).factory("tastyUtil",["debounce","setProperty","joinObjects",function(debounce,setProperty,joinObjects){return{debounce:debounce,setProperty:setProperty,joinObjects:joinObjects}}]),angular.module("ngTasty.service.debounce",[]).factory("debounce",["$timeout",function($timeout){return function(func,wait){var timeout;return function(){var context=this,args=arguments;$timeout.cancel(timeout),timeout=$timeout(function(){timeout=null,func.apply(context,args)},wait)}}}]),angular.module("ngTasty.service.setProperty",[]).factory("setProperty",function(){return function(objOne,objTwo,attrname){return"undefined"!=typeof objTwo[attrname]&&null!==objTwo[attrname]&&(objOne[attrname]=objTwo[attrname]),objOne}}),angular.module("ngTasty.service.joinObjects",[]).factory("joinObjects",["setProperty",function(setProperty){return function(objOne,objTwo){for(var attrname in objTwo)setProperty(objOne,objTwo,attrname);return objOne}}]),angular.module("ngTasty.table",["ngTasty.filter.cleanFieldName","ngTasty.filter.range","ngTasty.service.tastyUtil"]).constant("tableConfig",{query:{page:"page",count:"count",sortBy:"sort-by",sortOrder:"sort-order"},listItemsPerPage:[5,25,50,100],itemsPerPage:5,bindOnce:!0}).controller("TableController",["$scope","$attrs","$timeout","$filter","$parse","tableConfig","tastyUtil",function($scope,$attrs,$timeout,$filter,$parse,tableConfig,tastyUtil){"use strict";var listScopeToWatch;if(this.$scope=$scope,listScopeToWatch=["filters","query","resource","resourceCallback"],listScopeToWatch.forEach(function(scopeName){var lastValue,parentGet,compare,parentSet,parentValueWatch;$attrs[scopeName]&&(parentGet=$parse($attrs[scopeName]),compare=parentGet.literal?equals:function(a,b){return a===b||a!==a&&b!==b},parentSet=parentGet.assign,lastValue=$scope[scopeName]=parentGet($scope.$parent),parentValueWatch=function(parentValue){return compare(parentValue,$scope[scopeName])||(compare(parentValue,lastValue)?parentSet($scope.$parent,parentValue=$scope[scopeName]):$scope[scopeName]=parentValue),lastValue=parentValue},parentValueWatch.$stateful=!0,$scope.$parent.$watch($parse($attrs[scopeName],parentValueWatch),null,parentGet.literal))}),$scope.query=$scope.query||tableConfig.query,$scope.clientSide=!0,$scope.url="",$scope.header={columns:[]},$scope.rows=[],$scope.params={},$scope.pagination={count:5,page:1,pages:1,size:0},$scope.theadDirective=!1,$scope.paginationDirective=!1,!angular.isDefined($attrs.resource)&&!angular.isDefined($attrs.resourceCallback))throw"AngularJS tastyTable directive: need the resource or resource-callback attribute";if(angular.isDefined($attrs.resource)){if(!angular.isObject($scope.resource))throw"AngularJS tastyTable directive: the resource ("+$attrs.resource+") it's not an object";if(!$scope.resource.header&&!$scope.resource.rows)throw"AngularJS tastyTable directive: the resource ("+$attrs.resource+") has the property header or rows undefined"}if(angular.isDefined($attrs.resourceCallback)){if(!angular.isFunction($scope.resourceCallback))throw"AngularJS tastyTable directive: the resource-callback ("+$attrs.resourceCallback+") it's not a function";$scope.clientSide=!1}this.activate=function(directiveName){$scope[directiveName+"Directive"]=!0,$scope.params[directiveName]=!0},this.setParams=function(key,value){$scope.params[key]=value},this.bindOnce=tableConfig.bindOnce,$scope.setDirectivesValues=function(resource){var sortBy;if(!angular.isObject(resource))throw"AngularJS tastyTable directive: the resource it's not an object";if(!resource.header&&!resource.rows)throw"AngularJS tastyTable directive: the resource has the property header or rows undefined";1===Object.keys(resource.header[0]).length&&(resource.header=resource.header.map(function(header){var key=Object.keys(header)[0];return{key:key,name:header[key]}})),sortBy=resource.sortBy||$scope.params.sortBy,sortBy=sortBy||resource.header[0].key,$scope.header={columns:resource.header,sortBy:sortBy,sortOrder:resource.sortOrder||$scope.params.sortOrder},$scope.rows=resource.rows,$scope.pagination=resource.pagination||$scope.pagination},$scope.buildClientResource=function(){var fromRow,toRow,rowToShow,reverse,listSortBy;$scope.theadDirective&&(reverse="asc"===$scope.header.sortOrder?!1:!0,listSortBy=[function(item){return item[$scope.header.sortBy]}],$scope.header.columns[0].key!==$scope.header.sortBy&&listSortBy.push(function(item){return item[$scope.header.columns[0].key]}),$scope.rows=$filter("orderBy")($scope.rows,listSortBy,reverse)),$attrs.filters&&($scope.rows=$filter("filter")($scope.rows,$scope.filters)),$scope.paginationDirective&&($scope.pagination.page=$scope.params.page,$scope.pagination.count=$scope.params.count,$scope.pagination.size=$scope.rows.length,$scope.pagination.pages=Math.ceil($scope.rows.length/$scope.pagination.count),toRow=$scope.pagination.count*$scope.pagination.page,fromRow=toRow-$scope.pagination.count,fromRow>=0&&toRow>=0&&(rowToShow=$scope.rows.slice(fromRow,toRow),$scope.rows=rowToShow))},$scope.buildUrl=function(params,filters){var urlQuery,value;return urlQuery={},$scope.theadDirective&&(urlQuery=tastyUtil.setProperty(urlQuery,params,"sortBy"),urlQuery=tastyUtil.setProperty(urlQuery,params,"sortOrder")),$scope.paginationDirective&&(urlQuery=tastyUtil.setProperty(urlQuery,params,"page"),urlQuery=tastyUtil.setProperty(urlQuery,params,"count")),$attrs.filters&&(urlQuery=tastyUtil.joinObjects(urlQuery,filters)),Object.keys(urlQuery).map(function(key){return value=urlQuery[key],$scope.query[key]&&(key=$scope.query[key]),encodeURIComponent(key)+"="+encodeURIComponent(value)}).join("&")},$scope.updateClientSideResource=tastyUtil.debounce(function(){$scope.setDirectivesValues($scope.resource),$scope.buildClientResource()},100),$scope.updateServerSideResource=tastyUtil.debounce(function(){$scope.url=$scope.buildUrl($scope.params,$scope.filters),$scope.resourceCallback($scope.url,$scope.params).then(function(resource){$scope.setDirectivesValues(resource)})},100),$scope.initTable=function(){$scope.params.sortBy=void 0,$scope.params.sortOrder="asc",$scope.params.page=1,$scope.params.count=void 0,$scope.clientSide?$scope.updateClientSideResource():$scope.updateServerSideResource()},$attrs.filters&&$scope.$watch("filters",function(newValue,oldValue){newValue!==oldValue&&($scope.clientSide?$scope.updateClientSideResource():$scope.updateServerSideResource())},!0),$scope.$watchCollection("params",function(newValue,oldValue){newValue!==oldValue&&($scope.clientSide?$scope.updateClientSideResource():$scope.updateServerSideResource())}),$scope.resource&&$scope.$watch("resource",function(newValue,oldValue){newValue!==oldValue&&$scope.updateClientSideResource()},!0),$scope.initTable()}]).directive("tastyTable",function(){return{restrict:"A",scope:!0,controller:"TableController"}}).directive("tastyThead",["$filter",function($filter){return{restrict:"AE",require:"^tastyTable",scope:{notSortBy:"="},templateUrl:"template/table/head.html",link:function(scope,element,attrs,tastyTable){"use strict";tastyTable.activate("thead"),scope.bindOnce=tastyTable.bindOnce,scope.columns=[],scope.setColumns=function(){var lenHeader,width,active,sortable,sort;scope.columns=[],lenHeader=scope.header.columns.length,scope.header.columns.forEach(function(column){width=parseFloat((100/lenHeader).toFixed(2)),sortable=!0,active=!1,scope.notSortBy&&(sortable=scope.notSortBy.indexOf(column.key)<0),(column.key===scope.header.sortBy||"-"+column.key===scope.header.sortBy)&&(active=!0),sort=$filter("cleanFieldName")(column.key),scope.columns.push({key:column.key,name:column.name,active:active,sortable:sortable,width:{width:width+"%"},isSortUp:scope.header.sortBy==="-"+sort,isSortDown:scope.header.sortBy===sort})}),"dsc"===scope.header.sortOrder&&"-"!==scope.header.sortBy[0]&&(scope.header.sortBy="-"+scope.header.sortBy)},scope.sortBy=function(column){if(scope.notSortBy&&scope.notSortBy.indexOf(column.key)>=0)return!1;var columnName;columnName=$filter("cleanFieldName")(column.key),scope.header.sortBy==columnName?(scope.header.sortBy="-"+columnName,tastyTable.setParams("sortOrder","dsc")):(scope.header.sortBy=columnName,tastyTable.setParams("sortOrder","asc")),tastyTable.setParams("sortBy",column.key)},scope.classToShow=function(column){var listClassToShow=[];return column.sortable&&listClassToShow.push("sortable"),column.active&&listClassToShow.push("active"),listClassToShow},tastyTable.$scope.$watchCollection("header",function(newValue,oldValue){newValue&&newValue!==oldValue&&(scope.header=newValue,scope.setColumns())})}}}]).controller("TablePaginationController",["$scope","$attrs","tableConfig",function($scope,$attrs,tableConfig){angular.isDefined($attrs.itemsPerPage)&&($scope.itemsPerPage=$scope.$parent[$attrs.itemsPerPage]),angular.isDefined($attrs.listItemsPerPage)&&($scope.listItemsPerPage=$scope.$parent[$attrs.listItemsPerPage]),$scope.itemsPerPage=$scope.itemsPerPage||tableConfig.itemsPerPage,$scope.listItemsPerPage=$scope.listItemsPerPage||tableConfig.listItemsPerPage}]).directive("tastyPagination",["$filter",function($filter){return{restrict:"AE",require:"^tastyTable",scope:{},templateUrl:"template/table/pagination.html",controller:"TablePaginationController",link:function(scope,element,attrs,tastyTable){"use strict";var getPage,setCount,setPaginationRange,setPreviousRange,setRemainingRange,setPaginationRanges;tastyTable.activate("pagination"),scope.pagination={},scope.pagMinRange=1,scope.pagMaxRange=1,getPage=function(numPage){tastyTable.setParams("page",numPage)},setCount=function(count){var maxItems,page;maxItems=count*scope.pagination.page,maxItems>scope.pagination.size&&(page=Math.ceil(scope.pagination.size/count),tastyTable.setParams("page",page)),tastyTable.setParams("count",count)},setPaginationRange=function(){var currentPage;currentPage=scope.pagination.page,currentPage>scope.pagination.pages&&(currentPage=scope.pagination.pages),scope.pagMinRange=currentPage-2>0?currentPage-2:1,scope.pagMaxRange=currentPage+2,scope.pagination.page=currentPage,setPaginationRanges()},setPreviousRange=function(){return scope.pagHideMinRange===!0||scope.pagMinRange<1?!1:(scope.pagMaxRange=scope.pagMinRange,scope.pagMinRange=scope.pagMaxRange-scope.itemsPerPage,setPaginationRanges(),void 0)},setRemainingRange=function(){return scope.pagHideMaxRange===!0||scope.pagMaxRange>scope.pagination.pages?!1:(scope.pagMinRange=scope.pagMaxRange,scope.pagMaxRange=scope.pagMinRange+scope.itemsPerPage,scope.pagMaxRange>scope.pagination.pages&&(scope.pagMaxRange=scope.pagination.pages),scope.pagMinRange=scope.pagMaxRange-scope.itemsPerPage,setPaginationRanges(),void 0)},setPaginationRanges=function(){scope.pagMinRange=scope.pagMinRange>0?scope.pagMinRange:1,scope.pagMaxRange=scope.pagMinRange+5,scope.pagMaxRange>scope.pagination.pages&&(scope.pagMaxRange=scope.pagination.pages+1),scope.pagHideMinRange=scope.pagMinRange<=1,scope.pagHideMaxRange=scope.pagMaxRange>=scope.pagination.pages,scope.classPageMinRange=scope.pagHideMinRange?"disabled":"",scope.classPageMaxRange=scope.pagHideMaxRange?"disabled":"";for(var i=2;i<scope.listItemsPerPage.length;i++)if(scope.pagination.size<scope.listItemsPerPage[i]){scope.listItemsPerPageShow=scope.listItemsPerPage.slice(0,i);break}scope.rangePage=$filter("range")([],scope.pagMinRange,scope.pagMaxRange)},scope.classPaginationCount=function(count){return count==scope.pagination.count?"active":""},scope.classNumPage=function(numPage){return numPage==scope.pagination.page?"active":!1},scope.page={get:getPage,setCount:setCount,previous:setPreviousRange,remaining:setRemainingRange},tastyTable.$scope.$watchCollection("pagination",function(newValue,oldValue){newValue&&newValue!==oldValue&&(scope.pagination=newValue,setPaginationRange())}),scope.page.setCount(scope.itemsPerPage)}}}]),angular.module("template/table/head.html",[]).run(["$templateCache",function($templateCache){$templateCache.put("template/table/head.html",'<tr>\n  <th ng-repeat="column in columns track by $index" \n  ng-class="classToShow(column)"\n  ng-style="column.width" ng-click="sortBy(column)">\n    <span ng-bind="::column.name"></span>\n    <span ng-if="column.isSortUp" class="fa fa-sort-up"></span>\n    <span ng-if="column.isSortDown" class="fa fa-sort-down"></span>\n  </th> \n</tr>')}]),angular.module("template/table/pagination.html",[]).run(["$templateCache",function($templateCache){$templateCache.put("template/table/pagination.html",'<div class="row">\n  <div class="col-xs-3 text-left">\n    <div class="btn-group">\n      <button type="button" class="btn btn-default" \n      ng-repeat="count in listItemsPerPageShow" \n      ng-class="classPaginationCount(count)" \n      ng-click="page.setCount(count)" ng-bind="count"></button>\n    </div>\n  </div>\n  <div class="col-xs-6 text-center">\n    <ul class="pagination">\n      <li ng-class="classPageMinRange">\n        <span ng-click="page.previous()">&laquo;</span>\n      </li>\n      <li ng-repeat="numPage in rangePage" ng-class="classNumPage(numPage)">\n        <span ng-click="page.get(numPage)">\n          <span ng-bind="numPage"></span>\n          <span class="sr-only" ng-if="classNumPage(numPage)">(current)</span>\n        </span>\n      </li>\n      <li ng-class="classPageMaxRange">\n        <span ng-click="page.remaining()">&raquo;</span>\n      </li>\n    </ul>\n  </div>\n  <div class="col-xs-3 text-right">\n    <p>Page <span ng-bind="pagination.page"></span> \n    of <span ng-bind="pagination.pages"></span>,\n    of <span ng-bind="pagination.size"></span> entries</p>\n  </div>\n</div>')}]);