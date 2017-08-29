#!/bin/bash
set -e

export PGUSER=postgres
psql <<- EOSQL
    CREATE USER airflow;
    CREATE DATABASE airflow;
    CREATE DATABASE airflow_dag_data;
    GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;
    GRANT ALL PRIVILEGES ON DATABASE airflow_dag_data TO airflow;
EOSQL
