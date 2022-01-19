# Base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Defining ENV variables
ENV PROJECT_DIR /code

# cd to project_dir
WORKDIR ${PROJECT_DIR}

# 
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

RUN pip install pipenv && \
    pipenv lock --keep-outdated --requirements > /tmp/requirements.txt && \
    pip install -r /tmp/requirements.txt && \
    pip uninstall pipenv -y

# 
COPY ./app ${PROJECT_DIR}/app
COPY ./tests ${PROJECT_DIR}/tests

