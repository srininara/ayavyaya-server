var app = angular.module('expensesManager', ['ui.bootstrap', 'restangular', 'ngGrid', 'ngTagsInput', 'nvd3ChartDirectives']);

app.config(["RestangularProvider",
    function (RestangularProvider) {
        RestangularProvider.setBaseUrl('/ayavyaya/api/v1.0/');
        // TODO: Can I remove this interceptor
        RestangularProvider.addResponseInterceptor(function (data, operation, what, url, response, deferred) {
            var extractedData;
            // .. to look for getList operations
            if (operation === "getList") {
                // .. and handle the data and meta data
                extractedData = data[what];
                summaryKey = what + "Summary";
                extractedData.summary = data[summaryKey]
            } else {
                extractedData = data;
            }
            return extractedData;
        });
}]);

app.controller('ExpenseAggregatesCtrl', ['$scope', 'ExpenseAggregateService',
    function ($scope, ExpenseAggregateService) {
        ExpenseAggregateService.getList("daily").then(function (data) {
            $scope.dailyChartData = [{
                key: "Daily Aggregates",
                values: data
            }];
        });

        var colorCategory = ["green", "blue", "orange", "red"];

        $scope.colorFunction = function () {
            return function (d, i) {
                var colorIndex = 0;
                var y = d[1]
                if (y > 1000 && y <= 3000) colorIndex = 1;
                if (y > 3000 && y <= 10000) colorIndex = 2;
                if (y > 10000) colorIndex = 3;
                return colorCategory[colorIndex];
            };
        };

        $scope.xAxisTickFormatFunction = function () {
            return function (input) {
                var dateObj = new Date(input)
                var day = d3.time.format('%e')(dateObj);
                var month = d3.time.format('%b')(dateObj);
                return (day % 10 == 0) ? day + "-" + month : "";
            }
        };

        $scope.toolTipContentFunction = function () {
            return function (key, x, y, e, graph) {
                var dateObj = new Date(e.point[0]);
                var day = d3.time.format('%e')(dateObj);
                var month = d3.time.format('%b')(dateObj);
                return "<p><strong>Expense</strong></p><p>Rs. " + y + ' on ' + day + "-" + month + "</p>"
            }
        };

}]);


app.controller('ExpenseAggregatesMWCtrl', ['$scope', 'ExpenseAggregateService',
    function ($scope, ExpenseAggregateService) {
        ExpenseAggregateService.getList("dailyMonthWise").then(function (data) {
            $scope.dailyChartDataMWAll = data;
            $scope.dailyChartDataMWSummary = data.summary;
        });

        var colorCategory = ["green", "blue", "orange", "red"];

        $scope.colorFunction = function () {
            return function (d, i) {
                var colorIndex = 0;
                var y = d[1]
                if (y > 1000 && y <= 3000) colorIndex = 1;
                if (y > 3000 && y <= 10000) colorIndex = 2;
                if (y > 10000) colorIndex = 3;
                return colorCategory[colorIndex];
            };
        };

        $scope.xAxisTickFormatFunction = function () {
            return function (input) {
                var dateObj = new Date(input)
                var day = d3.time.format('%e')(dateObj);
                var month = d3.time.format('%b')(dateObj);
                return (day % 10 == 0) ? day + "-" + month : "";
            }
        };

        $scope.toolTipContentFunction = function () {
            return function (key, x, y, e, graph) {
                var dateObj = new Date(e.point[0]);
                var day = d3.time.format('%e')(dateObj);
                var month = d3.time.format('%b')(dateObj);
                return "<p><strong>Expense</strong></p><p>Rs. " + y + ' on ' + day + "-" + month + "</p>"
            }
        };

        $scope.xFunction = function () {
            return function (d) {
                return d[0];
            };
        }

}]);



app.controller('ExpenseCategoryClassificationCtrlMW', ['$scope', 'ExpenseClassificationService',
    function ($scope, ExpenseClassificationService) {
        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        ExpenseClassificationService.getList("category", {
            "split": "month"
        }).then(function (data) {
            $scope.categoryChartData = data; //[{key: "Daily Aggregates",values: data}];
        });
        $scope.xAxisTickFormatFunction = function () {
            return function (input) {
                if (typeof (input) === "number" && Math.floor(input) == input) {
                    return months[input - 1];
                } else {
                    return "";
                }
            }
        };

        $scope.toolTipContentFunction = function () {
            return function (key, x, y, e, graph) {
                return '<h3>' + key + '</h3>' +
                    '<p>' + y + ' in ' + months[e.point[0] - 1] + '</p>'
            }
        };

}]);


app.controller('ExpenseNatureClassificationCtrlMW', ['$scope', 'ExpenseClassificationService',
    function ($scope, ExpenseClassificationService) {
        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        ExpenseClassificationService.getList("nature", {
            "split": "month"
        }).then(function (data) {
            $scope.natureChartData = data; //[{key: "Daily Aggregates",values: data}];
        });
        $scope.xAxisTickFormatFunction = function () {
            return function (input) {
                if (typeof (input) === "number" && Math.floor(input) == input) {
                    return months[input - 1];
                } else {
                    return "";
                }
            }
        };

        $scope.toolTipContentFunction = function () {
            return function (key, x, y, e, graph) {
                return '<h3>' + key + '</h3>' +
                    '<p>' + y + ' in ' + months[e.point[0] - 1] + '</p>'
            }
        };

}]);

app.controller('ExpenseFrequencyClassificationCtrlMW', ['$scope', 'ExpenseClassificationService',
    function ($scope, ExpenseClassificationService) {
        var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        ExpenseClassificationService.getList("frequency", {
            "split": "month"
        }).then(function (data) {
            $scope.frequencyChartData = data; //[{key: "Daily Aggregates",values: data}];
        });
        $scope.xAxisTickFormatFunction = function () {
            return function (input) {
                if (typeof (input) === "number" && Math.floor(input) == input) {
                    return months[input - 1];
                } else {
                    return "";
                }
            }
        };

        $scope.toolTipContentFunction = function () {
            return function (key, x, y, e, graph) {
                return '<h3>' + key + '</h3>' +
                    '<p>' + y + ' in ' + months[e.point[0] - 1] + '</p>'
            }
        };

}]);


app.controller('ExpensesCtrl', ['$scope', '$filter', 'ExpenseService',
    function ($scope, $filter, ExpenseService) {
        $scope.expense = createInitializedExpense();
        $scope.expensesList = [];
        $scope.gridOptions = {
            data: 'expensesList',
            columnDefs: [
                {
                    field: 'expense_date',
                    displayName: 'Date'
                },
                {
                    field: 'description',
                    displayName: 'Description'
                },
                {
                    field: 'amount',
                    displayName: 'Amount'
                },
                {
                    displayName: 'Tags',
                    cellTemplate: '<div class="ngCellText"><span ng-repeat="tag in row.entity.tags">@{{tag.name}} </span></div>'
                },
    //{field:'id', displayName:'System Id'},
    ]
        };

        $scope.save = function () {
            $scope.expense.expense_date = $filter('date')($scope.expense.expense_date, 'yyyy-MM-dd');
            ExpenseService.post($scope.expense).then(function (addedExpense) {
                console.log("Done!");
                $scope.expensesList.push(addedExpense);
            }, function () {
                console.log("Something wrong");
            });
            $scope.expense = createInitializedExpense();
        };

        $scope.openDate = function ($event) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.opened = true;
        };

        function createInitializedExpense() {
            var expense = {};
            expense.description = "";
            expense.amount = 100;
            expense.expense_date = new Date();
            return expense;
        };

}]);

app.controller('ExpenseAggregatesBoxCtrl', ['$scope', 'ExpenseAggregateService',
    function ($scope, ExpenseAggregateService) {


        ExpenseAggregateService.getList("dailyMonthWiseStat").then(function (data) {
            $scope.myChartData = data;
        });
}]);

app.factory('ExpenseService', ['Restangular',
    function (Restangular) {
        return Restangular.all('expenses');
}]);

app.factory('ExpenseAggregateService', ['Restangular',
    function (Restangular) {
        return Restangular.one('expenseAggregates');
}]);

app.factory('ExpenseClassificationService', ['Restangular',
    function (Restangular) {
        return Restangular.one('expenseClassification');
}]);

app.directive('boxChart', function () {
    //  var chart = d3.fbox();
    return {
        restrict: 'E',
        replace: true,
        template: '<div class="chart"></div>',
        scope: {
            boxheight: '@',
            boxwidth: '@',
            rotate: '@',
            chartdata: '='
        },
        link: function (scope, element, attrs) {

            var chartEls = d3.select(element[0]).selectAll("svg");

            scope.$watch("chartdata", function (newVal) {

                function iqr(k) {
                    return function (d, i) {
                        var q1 = d.quartiles[0],
                            q3 = d.quartiles[2],
                            iqr = (q3 - q1) * k,
                            i = -1,
                            j = d.length;
                        while (d[++i] < q1 - iqr);
                        while (d[--j] > q3 + iqr);
                        return [i, j];
                    };
                }

                var boxheight = parseInt(attrs.boxheight);
                var boxwidth = parseInt(attrs.boxwidth);
                var rotate = attrs.rotate ? (attrs.rotate === "true") : false;

                var margin = {
                    top: 20,
                    right: 10,
                    bottom: 10,
                    left: 10
                };
                boxwidth_m = boxwidth - margin.left - margin.right,
                boxheight_m = boxheight - margin.top - margin.bottom;


                if (newVal) {

                    var chart = d3.fbox()
                        .whiskers(iqr(1.5))
                        .boxwidth(boxwidth_m)
                        .boxheight(boxheight_m)
                        .showOutliers(false)
                        .rotate(rotate);

                    var min = 0;
                        max = 0; //Initializing
                    var all_d = [];
                    var value = Number;
                    
                    for (var i = 0; i < newVal.length; i++) {
                        var monthData = newVal[i]["data"];
                        for (var j = 0;j < monthData.length; j++) {
                            var exp_val = monthData[j];
                            all_d.push(exp_val);
                        }
                    }
                    all_d = all_d.map(value).sort(d3.ascending);
//                    min = all_d[0], max = all_d[all_d.length -1];
                    min = d3.quantile(all_d, .125), max = d3.quantile(all_d, .875);


                    
                    chart.domain([min, max]);

                    chartEls.data(newVal)
                        .enter().append("svg")
                        .attr("class", rotate ? "box rotate" : "box")
                        .attr("height", boxwidth_m + margin.left + margin.right)
                        .attr("width", boxheight_m + margin.bottom + margin.top)
                        .append("g")
                        .attr("transform", "translate(" + margin.top + "," + margin.left + ")")
                        .call(chart);
                }
            });
        }
    }
});