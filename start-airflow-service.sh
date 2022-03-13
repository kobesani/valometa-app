#! /usr/bin/env bash

source './.airflow-env-3.8.10/bin/activate'

# export AIRFLOW_HOME="/mnt/sage/Development/valometa-app/.airflow-home"
# export AIRFLOW_HOME="${PWD}/.airflow-home"
# export AIRFLOW_HOME="${PWD}/valometa/airflow-home"
export AIRFLOW_HOME="/mnt/sage/Development/valometa-app/valometa/airflow-home"

airflow webserver -D
airflow scheduler -D

echo "Webserver running on localhost:8080"

