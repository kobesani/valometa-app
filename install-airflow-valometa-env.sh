#! /usr/bin/env bash

# Install development dependencies
devopt=$1

DEV="${devopt:=true}"

ENV_NAME=".airflow-env-$(python3 --version | cut -f2 -d' ')"

python3 -m venv ${ENV_NAME}

source ${ENV_NAME}/bin/activate


# Airflow needs a home. `~/airflow` is the default
export AIRFLOW_HOME="${PWD}/.airflow-home"

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.2.4

# For example: 3.8
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"

CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
wget -O "constraints-${PYTHON_VERSION}.txt" "${CONSTRAINT_URL}"

# some builds failed when calling bdist_wheel without the wheel module
pip install wheel --constraint "constraints-${PYTHON_VERSION}.txt"

# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.2.4/constraints-3.6.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" \
	--constraint "constraints-${PYTHON_VERSION}.txt"

# airflow webserver --port 8080

# airflow scheduler

pip install \
	requests \
	pandas \
	pydantic \
	parsel \
	streamlit \
	plotly \
	loguru \
	fastapi \
	uvicorn \
	python-multipart \
	psycopg2 \
	minify-html \
	--constraint "constraints-${PYTHON_VERSION}.txt"


if [ "${DEV}" = "true" ]; then
    echo "Installing development dependencies = ${DEV}"
    pip install \
        pytest \
		ipython \
	    jupyter \
	    pytest-cov \
	    black \
	    --constraint "constraints-${PYTHON_VERSION}.txt"
fi

airflow info

airflow db init

airflow users create \
    --username admin \
    --firstname Kobe \
    --lastname Rockata \
    --role Admin \
    --email harold.rockata@gmail.com

python generate-sqlite-connection.py
