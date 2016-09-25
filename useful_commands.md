### Testing Commands
* `py.test`
* `py.test -v`
* `py.test test/unit/test_date_utils.py`
* `py.test --pdb`
* `py.test --cov ayavyaya/ test/` : application code folder followed test code folder

### Linting Commands
* `pylint -f html ayavyaya > reports/linting/ayavyaya-$(date +%Y-%m-%d).html`
