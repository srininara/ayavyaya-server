var app = angular.module('expensesManager',['ui.bootstrap','restangular','ngGrid']);

app.config(["RestangularProvider",function(RestangularProvider){
	RestangularProvider.setBaseUrl('/grihasthi/api/v1.0/');
}]);

app.controller('ExpensesController', ['$scope', '$filter', 'ExpenseService', function($scope, $filter, ExpenseService) {
  $scope.expense = createInitializedExpense();
  $scope.expensesList = [];
  $scope.gridOptions = {
    data: 'expensesList',
    columnDefs: [
      {field:'id', displayName:'System Id'},
      {field:'description', displayName:'Description'},
      {field:'amount', displayName:'Amount'},
      {field:'expense_date', displayName:'Date'},
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
  }

  function createInitializedExpense() {
    var expense = {};
    expense.description = "";
    expense.amount = 100;
    expense.expense_date = new Date();
    return expense;
  }

}]);

app.factory('ExpenseService', ['Restangular', function(Restangular) {
  return Restangular.all('expenses');
}]);
