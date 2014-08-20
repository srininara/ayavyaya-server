var app = angular.module('expensesManager',['ui.bootstrap','restangular','ngGrid','ngTagsInput','nvd3ChartDirectives']);

app.config(["RestangularProvider",function(RestangularProvider){
	RestangularProvider.setBaseUrl('/grihasthi/api/v1.0/');
	RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
		var extractedData;
		// .. to look for getList operations
		if (operation === "getList") {
			// .. and handle the data and meta data
			extractedData = data[what];
		} else {
			extractedData = data;
		}
		return extractedData;
	});
}]);

app.controller('ExpenseAggregatesCtrl',['$scope','ExpenseAggregateService', function($scope, ExpenseAggregateService) {
	ExpenseAggregateService.getList("daily").then(function(data) {
		$scope.dailyChartData = [{key: "Daily Aggregates",values: data}];
	});

	var colorCategory = ["green", "blue", "red"];

	$scope.colorFunction = function() {
		return function(d, i) {
			var colorIndex = 0;
			var y = d[1]
			if (y>1000 && y<=3000) colorIndex = 1;
			if (y>3000) colorIndex = 2;
    	return colorCategory[colorIndex];
		};
	};

	$scope.xAxisTickFormatFunction = function() {
		return function(input) {
			var dateObj = new Date(input)
			var day = d3.time.format('%e')(dateObj);
			var month = d3.time.format('%b')(dateObj);
			return (day % 10 == 0)?day+"-"+month:"";
		}
	};

	$scope.toolTipContentFunction = function(){
		return function(key, x, y, e, graph) {
			var dateObj = new Date(e.point[0]);
			var day = d3.time.format('%e')(dateObj);
			var month = d3.time.format('%b')(dateObj);
	    return "<p><strong>Expense</strong></p><p>Rs. " + y + ' on ' + day+"-"+month + "</p>"
		}
	};

}]);

app.controller('ExpensesCtrl', ['$scope', '$filter', 'ExpenseService', function($scope, $filter, ExpenseService) {
	$scope.expense = createInitializedExpense();
	$scope.expensesList = [];
	$scope.gridOptions = {
		data: 'expensesList',
		columnDefs: [
		{field:'expense_date', displayName:'Date'},
		{field:'description', displayName:'Description'},
		{field:'amount', displayName:'Amount'},
		{displayName:'Tags', cellTemplate: '<div class="ngCellText"><span ng-repeat="tag in row.entity.tags">@{{tag.name}} </span></div>'},
		//{field:'id', displayName:'System Id'},
		]
	};

	$scope.save = function() {
		$scope.expense.expense_date = $filter('date')($scope.expense.expense_date, 'yyyy-MM-dd');
		ExpenseService.post($scope.expense).then(function(addedExpense){
			console.log("Done!");
			$scope.expensesList.push(addedExpense);
		},function(){
			console.log("Something wrong");
		});
		$scope.expense = createInitializedExpense();
	};

	$scope.openDate = function($event) {
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

app.factory('ExpenseService', ['Restangular', function(Restangular) {
	return Restangular.all('expenses');
}]);

app.factory('ExpenseAggregateService', ['Restangular', function(Restangular) {
	return Restangular.one('expenseAggregates');
}]);
