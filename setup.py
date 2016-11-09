import os

from setuptools import setup, find_packages

setup(
	name="ayavyaya",
	version="0.0.2",
	description="expense tracker",
	long_description=("Tracking expenses for the family"),
	url="http://www.nacnez.com/",
	license="",
	author="Srinivas Narayanan",
	author_email="srininara@gmail.com",
	packages=find_packages(exclude=["tests.*", "tests"]),
	include_package_data=True,
	zip_safe=False,
	package_data={
		'fe': 'ayavyaya/fe/*'
	},
	install_requires=[
		"alembic==0.7.4",
		"aniso8601==0.92",
		"click==3.3",
		"configobj==5.0.6",
		"Cython==0.21.2",
		"docopt==0.6.2",
		"docutils==0.12",
		"elasticsearch==1.6.0",
		"Flask==0.10.1",
		"Flask-Migrate==1.3.0",
		"Flask-RESTful==0.3.1",
		"Flask-Script==2.0.5",
		"Flask-SQLAlchemy==2.0",
		"gevent==1.0.2",
		"greenlet==0.4.10",
		"gunicorn==19.1.1",
		"itsdangerous==0.24",
		"jedi==0.8.1",
		"Jinja2==2.7.3",
		"Mako==1.0.1",
		"MarkupSafe==0.23",
		"numpy==1.9.1",
		"pgcli==0.19.2",
		"prompt-toolkit==0.26",
		"psycogreen==1.0",
		"psycopg2==2.5.4",
		"Pygments==2.0.2",
		"python-dateutil==2.4.0",
		"pytz==2014.10",
		"requests==2.5.1",
		"simplejson==3.6.5",
		"six==1.9.0",
		"SQLAlchemy==0.9.8",
		"sqlparse==0.1.14",
		"statistics==1.0.3.5",
		"toolz==0.7.1",
		"urllib3==1.12",
		"wcwidth==0.1.4",
		"Werkzeug==0.9.6",
		"wheel==0.24.0"
	],
	scripts=['bin/ayavyaya_mgr.py','bin/ayavyaya_g_starter.sh'],
	# entry_points = {
 #  		'console_scripts': [
 #    		'manager = scripts.rt_mgr:main'
 #  		]
 #  	},
	classifiers=[
    	"Private :: Do Not Upload"
	]
)
