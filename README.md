## [Wiki](https://gitlab.com/idealisgruppen/smartcity-portal/-/wikis/1.-System-description)

## How to set up:

### Prerequisites:

* Download and install Visual C++ Build Tools from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

* Download and install Python 3 64-Bit from: https://www.python.org/downloads/ 

* Download and install MySQL from: https://dev.mysql.com/downloads/mysql/  

### Cloning the repository:

Use git to clone the repository using:

```Bash
git clone https://gitlab.com/idealisgruppen/smartcity-portal.git
```

And change the directory to it with:

```bash
cd smartcity-portal
```

### Setting up pipenv:

Install pipenv using pip:

```bash
pip3 install pipenv
```

Set up the project using pipenv:

```bash
pipenv update
pipenv shell
```
**Note:** you can avoid using pipenv by installing each module using pip3 install <module>. Required modules are listed in the pipfile.

### Running the project on windows:

1. First run apidb.sql in your mysql server for the sensor and sensortype tables.

2. Then you must set up the config.py file, by entering your authorisation token
refresh token and "x-api-key" from the Telenorconnexion API. To get the API key, please contact your Telenor Connexion representative. You must also add your MySQL username and password.

3. If you wish to use the webinterface example, navigate to src\API\templates\webinterface.js and change the host variable to the URL you are planning to host from. See "host variable" in [Wiki - 5. Webinterface](https://gitlab.com/idealisgruppen/smartcity-portal/-/wikis/5.-Webinterface) for more information.

4. To populate the database with your sensors, sensor types, sensortables and start the sensordata retrieval process run the following. 

```bash
<python3 path> -m src.Backend.getdata
```

### OR (**RECOMMENDED**)

If you wish to run the script via task scheduler, set up the run.bat file in the main folder and assign it to a task schedule. Recommended interval 15 minutes.


5. To start the restAPI run the following.

```bash
<python3 path> -m src.API.restapi
```

### OR (**RECOMMENDED**)

Set up your own WSGI server to run the restapi.py file. See web.wsgi in src/API

## config.py

The authtoken and refreshtoken variables are optional to fill in, but an API-X key is required for the system to communicate with the "Managed IoT Cloud" REST API. Without an auth/refreshtoken, the system will require login credentials on each start.

sleepinterval specifies how often the system will gather data in the loop mode. Does nothing if the script is run with the raw arg.

waitforsync specifies if the system will wait until the minute in an hour hits 00, 15, 30 or 45 before starting the process. Does nothing if the script is run with the raw arg.

MySQL config requires a username and password to run, the default schema name in apidb.sql is "apidb", and does not require changing. The host is by default "localhost", and does also not require changing if the database is ran on a local server.