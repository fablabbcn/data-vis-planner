#!/bin/bash
set -e

export PGUSER=postgres
psql <<- EOSQL
    CREATE USER airflow;
    CREATE DATABASE airflow;
    GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
EOSQL