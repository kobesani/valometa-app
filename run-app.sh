#! /usr/bin/env bash

poetry run uvicorn valometa.api.routes:app --reload

