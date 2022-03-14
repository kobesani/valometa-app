#! /usr/bin/env bash

# ENV_NAME=".airflow-env-$(python3 --version | cut -f2 -d' ')"

# source "./.airflow-env-${ENV_NAME}/bin/activate"

source "${PWD}/.airflow-env-$(python3 --version | cut -f2 -d' ')/bin/activate"

AIRFLOW_VERSION=$(airflow version)

# export PYTHONPATH="${PWD}/valometa:${PYTHONPATH}"

# export PYTHONPATH="/mnt/sage/Development/valometa-app/valometa:${PYTHONPATH}"
export AIRFLOW_HOME="${PWD}/.airflow-${AIRFLOW_VERSION}-home"

PYTHONPATH=${PWD} airflow webserver -D
PYTHONPATH=${PWD} airflow scheduler -D

echo "Webserver running on localhost:8080"

