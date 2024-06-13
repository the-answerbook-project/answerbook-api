# API endpoint for Answerbook version 2.

## How to run the API via a command line for development

1. Clone this repository
2. Access directory via terminal and type
```poetry install```
```poetry shell```

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
