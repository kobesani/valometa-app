#! /usr/bin/env bash

#!/bin/bash

default_port=8000

function to_int {
    local -i num="10#${1}"
    echo "${num}"
}

function port_is_ok {
    local port="$1"
    local -i port_num=$(to_int "${port}" 2>/dev/null)

    if (( $port_num < 1 || $port_num > 65535 )) ; then
        echo $default_port
        return
    fi

    echo $port_num
}

port=$(port_is_ok $1)

poetry run uvicorn valometa.api.routes:app --reload --port ${port}
