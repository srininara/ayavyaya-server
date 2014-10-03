var app = angular.module('expensesManager',['ui.bootstrap','restangular','ngGrid','ngTagsInput','nvd3ChartDirectives']);

app.config(["RestangularProvider",function(RestangularProvider){
  RestangularProvider.setBaseUrl('/grihasthi/api/v1.0/');
  // TODO: Can I remove this interceptor
  RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
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

app.controller('ExpenseAggregatesCtrl',['$scope','ExpenseAggregateService', function($scope, ExpenseAggregateService) {
  ExpenseAggregateService.getList("daily").then(function(data) {
    $scope.dailyChartData = [{key: "Daily Aggregates",values: data}];
  });

  var colorCategory = ["green", "blue", "orange", "red"];

  $scope.colorFunction = function() {
    return function(d, i) {
      var colorIndex = 0;
      var y = d[1]
      if (y>1000 && y<=3000) colorIndex = 1;
      if (y>3000 && y<=10000) colorIndex = 2;
      if (y>10000) colorIndex = 3;
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


app.controller('ExpenseAggregatesMWCtrl',['$scope','ExpenseAggregateService', function($scope, ExpenseAggregateService) {
  ExpenseAggregateService.getList("dailyMonthWise").then(function(data) {
    $scope.dailyChartDataMWAll = data;
    $scope.dailyChartDataMWSummary = data.summary;
    // console.log($scope.dailyChartDataMWSummary);

//    $scope.dailyChartData = [{key: "Daily Aggregates",values: data}];
  });

  var colorCategory = ["green", "blue", "orange", "red"];

  $scope.colorFunction = function() {
    return function(d, i) {
      var colorIndex = 0;
      var y = d[1]
      if (y>1000 && y<=3000) colorIndex = 1;
      if (y>3000 && y<=10000) colorIndex = 2;
      if (y>10000) colorIndex = 3;
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

  $scope.xFunction = function(){
    return function(d){
      return d[0];
    };
  }

}]);



app.controller('ExpenseCategoryClassificationCtrl',['$scope','ExpenseClassificationService', function($scope, ExpenseClassificationService) {
  ExpenseClassificationService.getList("category").then(function(data) {
    $scope.categoryChartData = data;//[{key: "Daily Aggregates",values: data}];
  });

  $scope.xFunction = function(){
    return function(d) {
        return d.category_name;
    };
  }

  $scope.yFunction = function(){
    return function(d){
      return d.category_expenses;
    };
  }

  $scope.$on('elementMouseover.tooltip.directive', function(angularEvent, event){
    console.log("rr");  // TODO: Here is where we will launch a mechanism to show sub categories
  });



}]);


app.controller('ExpenseCategoryClassificationCtrlMW',['$scope','ExpenseClassificationService', function($scope, ExpenseClassificationService) {
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  ExpenseClassificationService.getList("category",{"split":"month"}).then(function(data) {
    $scope.categoryChartData = data;//[{key: "Daily Aggregates",values: data}];
  });
  $scope.xAxisTickFormatFunction = function() {
    return function(input) {
      if (typeof(input)==="number" && Math.floor(input)==input) {
        return months[input-1];
      } else {
        return "";
      }
    }
  };

  $scope.toolTipContentFunction = function(){
  	return function(key, x, y, e, graph) {
      	return  '<h3>' + key + '</h3>' +
                  '<p>' +  y + ' in ' + months[e.point[0]-1] + '</p>'
  	}
  };

}]);


app.controller('ExpenseSubcategoryClassificationCtrl',['$scope','ExpenseClassificationService', function($scope, ExpenseClassificationService) {
  ExpenseClassificationService.getList("subcategory").then(function(data) {
    $scope.subcategoryChartData = data;//[{key: "Daily Aggregates",values: data}];
  });

  $scope.xFunction = function(){
    return function(d) {
        return d.subcategory_name;
    };
  }

  $scope.yFunction = function(){
    return function(d){
      return d.subcategory_expenses;
    };
  }

  $scope.$on('elementMouseover.tooltip.directive', function(angularEvent, event){
    console.log("rr");  // TODO: Here is where we will launch a mechanism to show sub categories
  });



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

app.factory('ExpenseClassificationService', ['Restangular', function(Restangular) {
  return Restangular.one('expenseClassification');
}]);
