angular.module('expensesDashboard', ['ui.bootstrap', 'restangular', 'nvd3ChartDirectives'])
    .config(["RestangularProvider",
        function (RestangularProvider) {
            "use strict";
            RestangularProvider.setBaseUrl('/grihasthi/api/v1.0/');
        }])
    .controller('MonthCategoryStatsCtrl', ['$scope', 'MonthStatsCategoryService',
        function ($scope, MonthStatsCategoryService) {
            "use strict";
            var xAxisDataVarNameForCat = "category",
                yAxisDataVarNameForCat = "category_expenses",
                categorySpendChartKey = "Category Spend",
                xAxisDataVarNameForSubCat = "sub_category",
                yAxisDataVarNameForSubCat = "sub_category_expenses";

            function getDataFromService() {
                MonthStatsCategoryService.get("2014-12").then(function (data) {
                    $scope.monthCategoryRawData = [{
                        key: categorySpendChartKey,
                        values: data.categoryData
                    }];
                    $scope.monthSubCategoryRawData = [{
                        key: data.categoryData[0].category,
                        values: data.categoryData[0].sub_categories
                    }];
                });
            }
            getDataFromService();

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

            $scope.$on('elementClick.directive', function (angularEvent, event) {
                var mydata = event.point;
                if (mydata.category) {
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

        function getDataFromService() {
            var monthReq = $scope.requestedMonthYear.getFullYear()+"-"+ ($scope.requestedMonthYear.getMonth() + 1)
            MonthStatsDailyService.get(monthReq).then(function (data) {
                $scope.monthDailyRawData = [{
                    key: dailySpendChartKey,
                    values: data.dailyData
                    }];
                $scope.monthlySummary = data.summary;
            });
        }

        $scope.requestedMonthYear = new Date();
        $scope.requestedYear = 2014;

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
                maxKey = "maximum",
                color = d3.scale.linear()
                .domain([$scope.monthlySummary[minKey], $scope.monthlySummary[maxKey]])
                .range(["#88FF00", "#DD0000"]);
            return function (d, i) {
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

        $scope.$watch("requestedMonthYear", function (newVal) {
            getDataFromService();
        });

        $scope.openMP = function ($event) {
            $event.preventDefault();
            $event.stopPropagation();
            $scope.opened = true;
        };

        $scope.monthPickerOptions = {
            minMode: 'month'
        };
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
        ]);