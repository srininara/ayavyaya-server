### Release Steps for Ayavyaya Server
* Test on dev setup for both UI and mobile
* Change setup.py version number if applicable
* Check in code into push it to origin
* Create debian package for ayavyaya server
* Create a zip of current migrations folder
* Check if there are any changes to production config
* Create date of release folder inside releases
* Copy the debian package, migrations and production config into the created date folder under releases
* Run data backup from production database
* Destroy application vm using vagrant
* recreate application vm using vagrant and ansible
* login to application vm and run upgrade migrations
* Test out the new setup from web and mobile
* Tag git with the version number
