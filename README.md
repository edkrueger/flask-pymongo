# flask-pymongo
An template for a flask app with pymongo

## Environmental Variables
Copy `example.env` to `.env`.  
Put your mongo connection string into `.env` where indicated.  
Note: in order to use mLab's sandbox (free) instance, you must add `?retryWrites=false` to the end of the connection string. You'll have to do this in the .env file for local use and in the Heroku Config Vars for production.

## Dev Instructions
Run `pipenv install --dev` to install the env.  
Run `pipenv run pre-commit install` to initialize the git hooks.  
Run `pipenv run pre-commit run --all-files` if there are file that were committed before adding the git hooks.  
Activate the shell with: `pipenv shell`  
Lint with: `pylint app/`