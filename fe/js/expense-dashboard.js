angular.module('expensesDashboard', ['ui.bootstrap', 'restangular', 'nvd3ChartDirectives'])
    .config(["RestangularProvider",
        function (RestangularProvider) {
            "use strict";
            RestangularProvider.setBaseUrl('/grihasthi/api/v1.0/');
        }])
    .controller('MonthStatsCtrl', ['$scope',
        function ($scope) {
            "use strict";
            $scope.$watch("requestedMonthYear", function (newVal) {
                $scope.$broadcast("monthChanged", $scope.requestedMonthYear);
            });

            $scope.openMP = function ($event) {
                $event.preventDefault();
                $event.stopPropagation();
                $scope.opened = true;
            };

            $scope.monthPickerOptions = {
                minMode: 'month'
            };
            $scope.requestedMonthYear = new Date();

        }])
    .controller('MonthTopExpensesStatsCtrl', ['$scope', 'MonthStatsTopExpensesService',
        function ($scope, MonthStatsTopExpensesService) {
            "use strict";

            function getDataFromService(requestedDate) {
                var monthReq = requestedDate.getFullYear() + "-" + (requestedDate.getMonth() + 1)
                MonthStatsTopExpensesService.get(monthReq).then(function (data) {
                    $scope.topExpensesByValue = data.topExpensesByValue;
                    $scope.topExpensesByFrequency = data.topExpensesByFrequency;
                });
            }

            $scope.$on('monthChanged', function (event, reqDate) {
                getDataFromService(reqDate);
            });

        }
    ])
    .controller('MonthCategoryStatsCtrl', ['$scope', 'MonthStatsCategoryService',
        function ($scope, MonthStatsCategoryService) {
            "use strict";
            var xAxisDataVarNameForCat = "category",
                yAxisDataVarNameForCat = "category_expenses",
                categorySpendChartKey = "Category Spend",
                xAxisDataVarNameForSubCat = "sub_category",
                yAxisDataVarNameForSubCat = "sub_category_expenses";

            function getDataFromService(requestedDate) {
                var monthReq = requestedDate.getFullYear() + "-" + (requestedDate.getMonth() + 1)
                MonthStatsCategoryService.get(monthReq).then(function (data) {
                    if (data.categoryData.length > 0) {
                        $scope.monthCategoryRawData = [{
                            key: categorySpendChartKey,
                            values: data.categoryData
                        }];
                        $scope.monthSelectedCategoryRawData = data.categoryData[0];
                        $scope.monthSubCategoryRawData = [{
                            key: data.categoryData[0].category,
                            values: data.categoryData[0].sub_categories
                        }];
                    } else {
                        $scope.monthCategoryRawData = [];
                        $scope.monthSelectedCategoryRawData = {};
                        $scope.monthSubCategoryRawData = [];
                    }
                });
            }
            // TODO: Some of this needs to refactored to common place since it is repeating partially in daily expenses as well 
            $scope.createComparisonClasses = function (comparisonVal) {
                function isHigh() {
                    return comparisonVal === "Increased";
                }

                function isLow() {
                    return comparisonVal === "Decreased";
                }
                return ["glyphicon-" + (isHigh() ? "circle-arrow-up" : isLow()?"circle-arrow-down":"ok-sign"), "text-" + (isHigh() ? "danger" : isLow() ? "success" : "info")];
//                return ["glyphicon-thumbs-" + (isHigh() ? "down" : "up"), "text-" + (isHigh() ? "danger" : isLow() ? "success" : "info")];
            };

            $scope.xCatFunction = function () {
                return function (d) {
                    return d[xAxisDataVarNameForCat];
                };
            };
            $scope.yCatFunction = function () {
                return function (d) {
                    return d[yAxisDataVarNameForCat];
                };
            };
            $scope.xSubCatFunction = function () {
                return function (d) {
                    return d[xAxisDataVarNameForSubCat];
                };
            };
            $scope.ySubCatFunction = function () {
                return function (d) {
                    return d[yAxisDataVarNameForSubCat];
                };
            };

            $scope.$on('monthChanged', function (event, reqDate) {
                $scope.requestedDate = reqDate;
                $scope.prevMonthDate = new Date(reqDate.getFullYear(),reqDate.getMonth()-1,1);
                getDataFromService(reqDate);
            });

            $scope.$on('elementClick.directive', function (angularEvent, event) {
                var mydata = event.point;
                if (mydata.category) {
                    $scope.monthSelectedCategoryRawData = mydata;
                    $scope.monthSubCategoryRawData = [{
                        key: mydata.category,
                        values: mydata.sub_categories
                    }];
                    $scope.$apply();
                }
            });
}])
    .controller('MonthDailyStatsCtrl', ['$scope', 'MonthStatsDailyService',
            function ($scope, MonthStatsDailyService) {
            "use strict";

            var xAxisDataVarName = "expense_date",
                yAxisDataVarName = "daily_expense",
                dailySpendChartKey = "Daily Spend";

            function createComparisonAttributes(comparisonVal, prevMonthValue) {
                function isHigh() {
                    return comparisonVal === "Increased";
                }

                function isLow() {
                    return comparisonVal === "Decreased";
                }
                return {
//                    iconClass: "glyphicon-thumbs-" + (isHigh() ? "down" : "up"),
                    iconClass: "glyphicon-" + (isHigh() ? "circle-arrow-up" : isLow()?"circle-arrow-down":"ok-sign"),
                    colorClass: "text-" + (isHigh() ? "danger" : isLow() ? "success" : "info"),
                    title: comparisonVal + " - last month: " + prevMonthValue
                }
            }

            function doComparisons() {
                $scope.maxAttrs =
                    $scope.avgAttrs =
                    $scope.medianAttrs = {
                        iconClass: "glyphicon-info-sign",
                        colorClass: "text-info",
                        title: "No data to compare"
                };
                if ($scope.comparison && Object.keys($scope.comparison).length > 0) {
                    var pMS = $scope.prevMonthSummary;
                    var comp = $scope.comparison;
                    $scope.maxAttrs = createComparisonAttributes(comp.maximum, pMS.maximum);
                    $scope.avgAttrs = createComparisonAttributes(comp.mean, pMS.mean);
                    $scope.medianAttrs = createComparisonAttributes(comp.median, pMS.median);
                }
            }


            function getDataFromService(requestedDate) {
                var monthReq = requestedDate.getFullYear() + "-" + (requestedDate.getMonth() + 1)
                MonthStatsDailyService.get(monthReq).then(function (data) {
                    if (data.dailyData.length > 0) {
                        $scope.monthDailyRawData = [{
                            key: dailySpendChartKey,
                            values: data.dailyData
                    }];
                        $scope.monthlySummary = data.summary;
                        $scope.prevMonthSummary = data.prev_month_summary;
                        $scope.comparison = data.comparison
                        doComparisons();
                    } else {
                        $scope.monthDailyRawData = []
                        $scope.monthlySummary = {}
                        $scope.prevMonthSummary = {}
                    }
                });
            }

            $scope.xFunction = function () {
                return function (d) {
                    return d[xAxisDataVarName];
                };
            };
            $scope.yFunction = function () {
                return function (d) {
                    return d[yAxisDataVarName];
                };
            };

            $scope.colorFunction = function () {
                var minKey = "minimum",
                    maxKey = "maximum";
                return function (d, i) {
                    // NOTE: Not sure if this is the right place for this.
                    var color = d3.scale.linear()
                        .domain([$scope.monthlySummary[minKey], $scope.monthlySummary[maxKey]])
                        .range(["#88FF00", "#DD0000"]);

                    var y = d[yAxisDataVarName];
                    return color(y);
                };
            };

            $scope.xAxisTickFormatFunction = function () {
                var dailyDataXAxisTickInterval = 5;
                return function (input) {
                    var dateObj = new Date(input),
                        day = d3.time.format('%e')(dateObj),
                        day_to_show = d3.time.format('%e-%b')(dateObj);
                    return (day % dailyDataXAxisTickInterval === 0) ? day_to_show : "";
                };
            };

            $scope.toolTipContentFunction = function () {
                return function (key, x, y, e, graph) {
                    var dateObj = new Date(e.point[xAxisDataVarName]),
                        day = d3.time.format('%e-%b-%Y')(dateObj);
                    return "<p><strong>" + key + "</strong></p><p>Rs. " + y + ' on ' + day + "</p>";
                };
            };

            $scope.showSummary = function () {
                return $scope.monthlySummary && Object.keys($scope.monthlySummary).length > 0;
            }

            $scope.$on('monthChanged', function (event, reqDate) {
                getDataFromService(reqDate);
            });

    }
    ])
    .factory('MonthStatsDailyService', ['Restangular',
        function (Restangular) {
            "use strict";
            return Restangular.all('monthStatsDaily');
        }
        ])
    .factory('MonthStatsCategoryService', ['Restangular',
        function (Restangular) {
            "use strict";
            return Restangular.all('monthStatsCategory');
        }
    ])
    .factory('MonthStatsTopExpensesService', ['Restangular',
        function (Restangular) {
            "use strict";
            return Restangular.all('monthStatsTopExpenses');
        }
    ]);