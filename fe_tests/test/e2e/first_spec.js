describe('e2e: main', function() {

  var ptor;

  beforeEach(function() {
    browser.get('http://127.0.0.1:5000/grihasthi/fe/index.html');
    ptor = protractor.getInstance();
  });

  it('should load the home page', function() {
    var ele = by.id('home');
    expect(ptor.isElementPresent(ele)).toBe(true);
  });
});
