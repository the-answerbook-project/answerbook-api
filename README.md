# API endpoint for Answerbook version 2.

## Running tests
To run tests independent of your setup, do:
```shell
docker compose run tests
```

## How to run the API via a command line for development
1. Clone this repository & `cd` into it
2. Ensure you are on python 3.12 - we recommend using `pyenv` to manage python versions:
```pyenv install 3.12```
```pyenv local 3.12```
4. Install dependencies using `poetry`:
```poetry install```
```poetry shell```
5. If you are going to contribute, please install the pre-commit hooks:
```pre-commit install```

The above commands download and install
the required libraries for the project and activate the
virtual environment.

3. To run the app from the command line type:
```uvicorn main:app --reload```

The API should be up and running (localhost) at:

http://127.0.0.1:8000/

## Pycharm config settings
 * Create a python run configuration
 * Module name: uvicorn
 * Parameters: main:app --reload
 * Python interpreter: This should pick up "Poetry"...
 * Working directory: /..../answerbook-api

Basic Poetry usage here:
https://python-poetry.org/docs/basic-usage/
