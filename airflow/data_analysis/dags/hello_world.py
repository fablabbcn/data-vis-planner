# -*- encoding: utf-8 -*-
#
# Template for Airflow DAGS
#
# Author: Massimo Menichinelli
# E-mail: info@openp2pdesign.org - massimo@fablabbcn.org
# License: MIT
#
#

# Import various airflow modules
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.hooks.postgres_hook import PostgresHook
# Load variables stored in Airflow
# for passwords, access to databases, API keys and so on...
from airflow.models import Variable
# You can load variables in this way:
# my_new_python_variable = Variable.get("variable_name_in_airflow_UI")

# Work with time
from datetime import datetime
# Work with JSON
import json

# Example: load data from Fablabs.io
from makerlabs import fablabs_io


# DAG name (for the DAG but also for the database)
dag_name = "hello_world"
pg_hook = PostgresHook(postgres_conn_id='postgres_data')
table_raw_name = dag_name+"_raw"

# Setup the Python functions for the operators

# This function loads data and saves it into the raw collection
def first_def():
    global table_raw_name
    global pg_hook
    # Get raw data from Fablabs.io, as an example
    data = fablabs_io.get_labs(format="dict")
    pg_command = """CREATE TABLE IF NOT EXISTS %s ( id integer NOT NULL, board_id integer NOT NULL, data jsonb );"""
    pg_hook.run(pg_command, parameters=[table_raw_name])
    pg_command = """INSERT INTO %s VALUES ( %s );"""
    # Transform the dict into a string for PostgreSQL
    data2 = json.dumps(data)
    pg_hook.run(pg_command, parameters=[table_raw_name, data2])
    return "Data saved successfully."

# This function cleans raw data, transforms it for the visualization
def second_def():
    # Load data from the raw collection
    # Clean the data for the Meteor visualisation
    return "Data prepared for the visualization successfully."


# Setup the DAG
#
# schedule_interval uses the cron format
#
# * * * * * *
# | | | | | |
# | | | | | +-- Year              (range: 1900-3000)
# | | | | +---- Day of the Week   (range: 1-7, 1 standing for Monday)
# | | | +------ Month of the Year (range: 1-12)
# | | +-------- Day of the Month  (range: 1-31)
# | +---------- Hour              (range: 0-23)
# +------------ Minute            (range: 0-59)
#
# See more: http://www.nncron.ru/help/EN/working/cron-format.htm

dag = DAG(dag_name,
          description="Simple template for DAGs",
          schedule_interval="@hourly",
          start_date=datetime(2017, 8, 11, 14, 05),
          catchup=False
          )

# Setup the operators of the DAG
first_operator = PythonOperator(
    task_id="hello_task_01",
    python_callable=first_def,
    dag=dag)

# second_operator = PythonOperator(
#     task_id="hello_task_02", python_callable=second_def, dag=dag)
#
# third_operator = PythonOperator(
#     task_id="hello_task_03", python_callable=third_def, dag=dag)

fourth_operator = BashOperator(
    task_id='postgres2mongo',
    bash_command='python /usr/local/airflow/dags/postgres2mongo.py',
    dag=dag)


# Setup the flow of operators in the DAG
# first_operator >> second_operator >> third_operator
first_operator << fourth_operator
