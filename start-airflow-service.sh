#! /usr/bin/env bash

source './.airflow-env-3.8.10/bin/activate'

AIRFLOW_VERSION=$(airflow version)
# export AIRFLOW_HOME="${PWD}/.airflow-${AIRFLOW_VERSION}-home"
export PYTHONPATH="/mnt/sage/Development/valometa-app/valometa:${PYTHONPATH}"

# export AIRFLOW_HOME="/mnt/sage/Development/valometa-app/.airflow-home"
# export AIRFLOW_HOME="${PWD}/.airflow-home"
# export AIRFLOW_HOME="${PWD}/valometa/airflow-home"

# export AIRFLOW_HOME="/mnt/sage/Development/valometa-app/valometa/airflow-home"
export AIRFLOW_HOME="/mnt/sage/Development/valometa-app/.airflow-2.2.4-home"

airflow webserver -D
airflow scheduler -D

echo "Webserver running on localhost:8080"

