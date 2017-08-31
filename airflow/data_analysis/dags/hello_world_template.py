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
from datetime import datetime, timedelta
# Work with JSON
import json

# Example: load data from Fablabs.io
from makerlabs import fablabs_io


# DAG name (for the DAG but also for the database)
dag_name = "hello_world_template"
# Connection to the PostgreSQL, to be defined in the Airflow UI
pg_hook = PostgresHook(postgres_conn_id="postgres_data")


# Setup the Python functions for the operators

# This function create the db table if it does not exist
# and update the id of the row if there are previous ones with the same name
def setup_db(**kwargs):
    global pg_hook
    global dag_name
    # Create the dag_dag table for storing all the data
    pg_command = """CREATE TABLE IF NOT EXISTS dag_dag ( id CHAR(50) PRIMARY KEY, raw_data jsonb, clean_data jsonb, type CHAR(50), notes varchar(200), created_at timestamp DEFAULT NOW(), updated_at timestamp DEFAULT NOW() );"""
    pg_hook.run(pg_command)
    # A function for updating the updated_at column at each UPDATE
    pg_command = """CREATE OR REPLACE FUNCTION update_at_function()
    RETURNS TRIGGER AS $$
    BEGIN
       NEW.updated_at = NOW();
       RETURN NEW;
    END;
    $$ language 'plpgsql';"""
    pg_hook.run(pg_command)
    # A trigger for calling the above function
    pg_command = """DROP TRIGGER IF EXISTS update_column ON dag_dag"""
    pg_hook.run(pg_command)
    pg_command = """CREATE TRIGGER update_column BEFORE UPDATE ON dag_dag FOR EACH ROW EXECUTE PROCEDURE update_at_function();"""
    pg_hook.run(pg_command)
    # Check if a row with the same id exists
    pg_command = """SELECT id FROM dag_dag WHERE id LIKE %s"""
    previous_dags_same_name = []
    search_term = "%" + dag_name + "%"
    # If it exists, add consecutive number to it
    for i in pg_hook.get_records(pg_command, parameters=[search_term]):
        previous_dags_same_name.append(i[0].rstrip())
    if len(previous_dags_same_name) > 0:
        if previous_dags_same_name[-1][-1].isdigit():
            new_id = dag_name + str(int(previous_dags_same_name[-1][-1]) + 1)
        else:
            new_id = dag_name + "1"
    else:
        new_id = dag_name
    # Return the updated id name
    return new_id


# This function loads data and saves it into the raw collection
def get_raw_data(**kwargs):
    global pg_hook
    ti = kwargs["ti"]
    new_id = ti.xcom_pull(task_ids="hello_task_01")
    # Get raw data from Fablabs.io, as an example
    data = fablabs_io.get_labs(format="dict")
    # Transform the dict into a string for PostgreSQL
    data = json.dumps(data)
    # Save the data
    pg_command = """INSERT INTO dag_dag ( id, raw_data) VALUES ( %s, %s )"""
    pg_hook.run(pg_command, parameters=[new_id, data])
    return "Raw data saved successfully."


# This function cleans raw data, transforms it for the visualisation
def clean_data(**kwargs):
    global pg_hook
    ti = kwargs["ti"]
    new_id = ti.xcom_pull(task_ids="hello_task_01")
    # Load data from the raw_data column, it's only 1 value
    pg_command = """SELECT raw_data FROM dag_dag WHERE id = %s"""
    data = pg_hook.get_records(pg_command, parameters=[new_id])[0][0]
    # clean the data for the Meteor visualisation
    data = {"number of labs": len(data)}
    # Transform the dict into a string for PostgreSQL
    data = json.dumps(data)
    # Save the data
    pg_command = """UPDATE dag_dag SET clean_data = %s WHERE id = %s"""
    pg_hook.run(pg_command, parameters=[data, new_id])
    return "Data prepared for the visualisation successfully."


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
#
# Or datetime.timedelta
# See more: https://docs.python.org/2/library/datetime.html#datetime.timedelta
#

schedule_interval = timedelta(minutes=20)

dag = DAG(dag_name,
          description="Simple template for DAGs",
          schedule_interval=schedule_interval,
          start_date=datetime.now() - schedule_interval,
          catchup=False)

# Setup the operators of the DAG
first_operator = PythonOperator(
    task_id="hello_task_01",
    python_callable=setup_db,
    provide_context=True,
    dag=dag)

second_operator = PythonOperator(
    task_id="hello_task_02",
    python_callable=get_raw_data,
    provide_context=True,
    dag=dag)

third_operator = PythonOperator(
    task_id="hello_task_03",
    python_callable=clean_data,
    provide_context=True,
    dag=dag)

fourth_operator = BashOperator(
    task_id="postgres2mongo",
    bash_command="python /usr/local/airflow/dags/postgres2mongo.py" + " --id=" +
    "{{ ti.xcom_pull('hello_task_01') }}",
    dag=dag)

# Setup the flow of operators in the DAG
first_operator >> second_operator >> third_operator >> fourth_operator
