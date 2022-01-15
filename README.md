# fast-api-tutorial
This repo is an blank fastapi application to be used as base for other project.

The app runs in `docker` so it works no matter what your local machine is. 

* run the app first time: `bash bash_commands/run_app.sh`. This setups the application which is a 3 component app: rest_api, dev_db and test_db

If you want to run the tests go to the `rest_api app` bash with the command `docker exec -it <container_id> bash` and
then run `pytest`. (note that the `container_id` can be getted using the `docker ps` command)

* stop the app: run `docker-compose stop`

* start the app: run `docker-compose up -d`
## Models represents a table within the database
## BaseModel is a class used by Pydantic to define strictly types dataclasses