
var workflow = angular.module('mainapp');
//configureModule(workflow);
workflow.controller('FlowchartController', ['$scope', FlowchartController]);
//.controller('SamplesController', ['$scope','Sample', SamplesController]);
function FlowchartController($scope) {
	var chartDataModel = {

	        nodes: [
	            {
	                name: "Example Node 1",
	                id: 0,
	                x: 0,
	                y: 0,
	                inputConnectors: [
	                    {
	                        name: "A",
	                    },
	                    {
	                        name: "B",
	                    },
	                    {
	                        name: "C",
	                    },
	                ],
	                outputConnectors: [
	                    {
	                        name: "A",
	                    },
	                    {
	                        name: "B",
	                    },
	                    {
	                        name: "C",
	                    },
	                ],
	            },

	            {
	                name: "Example Node 2",
	                id: 1,
	                x: 400,
	                y: 200,
	                inputConnectors: [
	                    {
	                        name: "A",
	                    },
	                    {
	                        name: "B",
	                    },
	                    {
	                        name: "C",
	                    },
	                ],
	                outputConnectors: [
	                    {
	                        name: "A",
	                    },
	                    {
	                        name: "B",
	                    },
	                    {
	                        name: "C",
	                    },
	                ],
	            },

	        ],

	        connections: [
	            {
	                source: {
	                    nodeID: 0,
	                    connectorIndex: 1,
	                },

	                dest: {
	                    nodeID: 1,
	                    connectorIndex: 2,
	                },
	            },


	        ]
	    };
	$scope.chartViewModel = new flowchart.ChartViewModel(chartDataModel);
	
}

