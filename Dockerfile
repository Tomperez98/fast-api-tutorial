# Base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Defining ENV variables
ENV PROJECT_DIR /code

# cd to project_dir
WORKDIR ${PROJECT_DIR}

# 
COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

RUN pip install pipenv && \
    apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
    pipenv install --deploy --system && \
    apt-get remove -y gcc python3-dev libssl-dev && \
    apt-get autoremove -y && \
    pip uninstall pipenv -y

# 
COPY ./app ${PROJECT_DIR}/app
COPY ./tests ${PROJECT_DIR}/tests

