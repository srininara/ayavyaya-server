### Testing Commands
* `py.test`
* `py.test -v`
* `py.test test/unit/test_date_utils.py`
* `py.test --pdb`
* `py.test --cov ayavyaya/ test/` : application code folder followed test code folder

### Linting Commands
* `pylint -f html ayavyaya > reports/linting/ayavyaya-$(date +%Y-%m-%d).html`

### Debian Packaging Commands
* `dpkg-buildpackage -us -uc`

### Running Migrations
`/usr/share/python/ayavyaya/bin/ayavyaya_mgr.py db upgrade`

### Running Acceptance Tests
    # Run tests against flask runserver in dev virtualenv
    source ./virtualenvs/dev/bin/activate    
    ./ayavyaya_devruner.py runserver

    # Run behave
    ./test/run_behave.sh

### Running Perf Tests
    # Start the gunicorn server under dev virtualenv
    source ./virtualenvs/dev/bin/activate
    ./ayavyaya_dev.sh

    # Start locust under perf virtualenv
    source ./virtualenvs/perf/bin/activate
    ./test/run_locust.sh my_perf_test.py

