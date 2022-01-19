# fast-api-tutorial
This repo is an blank fastapi application to be used as base for other project.

The app runs in `docker` so it works no matter what your local machine is. 

* run the app first time: `bash bash_commands/run_app.sh`. This setups the application which is a 4 component app: rest_api, dev_db and test_db and a pgadmin so we have a UI over the databases.

If you want to run the tests go to the `rest_api app` bash with the command `docker exec -it <container_id> bash` and
then run `pytest`. (note that the `container_id` can be getted using the `docker ps` command)

* stop the app: run `docker-compose stop`

* start the app: run `docker-compose up -d`

## Managed dependencies

The proyect used to have a `requirements.txt` file with dependencies. Not we are using [`pipenv`](https://pipenv.pypa.io/en/latest/) to handle dependencies. In case you don't have pipenv installed and wanted to setup a development environment locally just install pipenv and run the command `pipenv shell` in the same file location than `Pipfile` and `Pipfile.locks` (**IMPORTANT** make sure you have a local python version that matches the required version. I use `conda` for that, and when I run `pipenv shell` I make sure I'm in a conda python version that matches the required one)

## Env variables
So the app can runned it expects a `.env` within the following location: `app/config/app.env`.
This a sample for the required `app.env` file: 

```text
SECRET_KEY= generated using `openssl rand -base64 32` command
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES= Whatever int you want (I use 30)
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
HOST_DEV_DB=dev_database --> must match docker-compose component
HOST_TEST_DB=test_database --> must match docker-compose component
EXPOSED_PORT= exposed port (default 5432)
POSTGRES_DB= database to use (example. app_database)
```

# Development inside docker container
Follow this tutorial: https://code.visualstudio.com/docs/remote/containers-tutorial

**NOTE:** I didn't worked that well for me on Windows but runs smoothly on Linux and MacOS

# Development locally
The `docker-compose.yml` setups a volume pointing to the repo. So even if you want to develop
locally code changes will be automatically detected by the container running the `rest_api` service.

Docker code and local code are sync, basically.

## Models represents a table within the database
## BaseModel is a class used by Pydantic to define strictly types dataclasses