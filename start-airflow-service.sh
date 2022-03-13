#! /usr/bin/env bash

source './.airflow-env-3.8.10/bin/activate'

airflow webserver -D
airflow scheduler -D

echo "Webserver running on localhost:8080"
