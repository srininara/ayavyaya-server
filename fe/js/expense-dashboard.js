angular.module('expensesDashboard', ['ui.bootstrap', 'restangular', 'nvd3ChartDirectives'])
    .config(["RestangularProvider",
        function (RestangularProvider) {
            RestangularProvider.setBaseUrl('/grihasthi/api/v1.0/');
            // TODO: Can I remove this interceptor
            RestangularProvider.addResponseInterceptor(function (data, operation, what, url, response, deferred) {
                var extractedData;
                // .. to look for getList operations
                if (operation === "getList") {
                    // .. and handle the data and meta data
                    extractedData = data[what];
                    //                    summaryKey = what + "Summary";
                    //                    extractedData.summary = data[summaryKey]
                } else {
                    extractedData = data;
                }
                return extractedData;
            });
        }])
    .controller('MonthDailyStatsCtrl', ['$scope', 'MonthStatsDailyService',
        function ($scope, MonthStatsDailyService) {
            var xAxisDataVarName = "expense_date";
            var yAxisDataVarName = "daily_expense";
            var dailySpendChartKey = "Daily Spend";

            MonthStatsDailyService.get("2014-12").then(function (data) {
                $scope.monthDailyRawData = [{
                    key: dailySpendChartKey,
                    values: data.dailyData
                }];
                $scope.monthlySummary = data.summary;

            });

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
                var color = d3.scale.linear()
                    .domain([$scope.monthlySummary[minKey], $scope.monthlySummary[maxKey]])
                    .range(["#0000AA", "#AA0000"]);
                return function (d, i) {
                    var y = d[yAxisDataVarName]
                    return color(y);
                };
            };

            $scope.xAxisTickFormatFunction = function () {
                var dailyDataXAxisTickInterval = 5;
                return function (input) {
                    var dateObj = new Date(input)
                    var day = d3.time.format('%e')(dateObj);
                    var day_to_show = d3.time.format('%e-%b')(dateObj);
                    return (day % dailyDataXAxisTickInterval == 0) ? day_to_show : "";
                }
            };

            $scope.toolTipContentFunction = function () {
                return function (key, x, y, e, graph) {
                    var dateObj = new Date(e.point[xAxisDataVarName]);
                    var day = d3.time.format('%e-%b-%Y')(dateObj);
                    return "<p><strong>" + key + "</strong></p><p>Rs. " + y + ' on ' + day + "</p>"
                };
            };
        }
    ])
    .factory('MonthStatsDailyService', ['Restangular',
        function (Restangular) {
            return Restangular.all('monthStatsDaily');
        }
    ]);