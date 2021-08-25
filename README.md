# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Environment variables

This project integrates with a trello board. To use, you will need an account with https://trello.com/en-GB, and the following variables must be populated in the `.env` file.

* `TRELLO_ACCOUNT_KEY` - Your Trello account key. This can be found at https://trello.com/app-key after logging in.
* `TRELLO_SECRET_KEY` - Your Trello secret token
* `BOARD_ID` - The ID of the board to save cards
* `TODO_LIST_ID` - The id of the "To Do" list within the board
* `IN_PROGRESS_LIST_ID` - The id of the "Doing" list within the board
* `DONE_LIST_ID` - the id of the "Done" list within the board

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Unit testing

This project uses `pytest` to unit test the code, in addition to `selenium` to carry out end to end tests.
In order to run the Selenium tests, please ensure that the [`chromedriver`](https://chromedriver.chromium.org/) has been installed in the python installation directory.
To run, ensure that pytest has been inttalled, then in a console navigate to the root directory of the project, and type:

```
poetry run pytest
```

This should run all tests and if successful should display the number of passed tests.

## Deployment

This project uses Vagrant to spin up a virtual machines with the app installed. Please ensure that this is installed locally before running `vagrant up` from the root directory of this project.


## Documentation

C4 model diagrams can be found in the `documentation` folder. The context, container and component diagrams are in SVG format and can be edited using draw.io.
The class diagram is saved in [https://plantuml.com/](plantUML) format; the resulting SVG is saved in `code.svg`. To convert the file to an SVG image, you will need the plantuml jar file installed locally along with the java runtime environment. Run the following from the project root directory:

```
$ java -jar /path/to/plantuml.jar -tsvg  documentation/code.puml
```