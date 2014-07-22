describe('e2e: main', function() {

  var ptor;

  beforeEach(function() {
    browser.get('http://127.0.0.1:5000/grihasthi/fe/index.html');
    ptor = protractor.getInstance();
    ptor.ignoreSynchronization = true;
  });

  it('should load the expenses manager page', function() {
    var ele = by.id('expenses-manager');
    expect(ptor.isElementPresent(ele)).toBe(true);
  });

  it('should be able to enter expense details and submit', function() {
    element(by.model('expense.description')).clear();
    element(by.model('expense.description')).sendKeys('Snacks');
    element(by.model('expense.amount')).clear();
    element(by.model('expense.amount')).sendKeys(110);
    element(by.model('expense.expense_date')).click();
    element(by.id('expense-save')).click();
    element.all(by.binding('row.entity.description')).each(function(cell){
      browser.sleep(500);
      cell.click();
      cell.getText().then(function(text){
        expect(text).toBe('Snacks');
      });
    });

    element.all(by.binding('row.entity.amount')).each(function(cell){
      browser.sleep(500);
      cell.click();
      cell.getText().then(function(text){
        expect(text).toBe('110.00');
      });
    });



  });

});
