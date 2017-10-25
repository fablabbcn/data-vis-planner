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
# from airflow.models import Variable
# You can load variables in this way:
# my_new_python_variable = Variable.get("variable_name_in_airflow_UI")

# Work with time
from datetime import datetime, timedelta

# DAG name (for the DAG but also for the database)
dag_name = "hello_world_twitter_stream"
# Connection to the PostgreSQL, to be defined in the Airflow UI
pg_hook = PostgresHook(postgres_conn_id="postgres_data")

# Setup the Python functions for the operators


# This function create the db table if it does not exist
# and update the id of the row if there are previous ones with the same name
def setup_db(**kwargs):
    global pg_hook
    global dag_name
    # Create the dag_dag table for storing all the data
    pg_command = """CREATE TABLE IF NOT EXISTS dag_dag ( id CHAR(50) PRIMARY KEY, track varchar(140), type CHAR(50), title varchar(120), text varchar(400), footer varchar(400), created_at timestamp DEFAULT NOW(), updated_at timestamp DEFAULT NOW() );"""
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

    # Save the data
    dag_track = "python"
    dag_type = "twitter_stream"
    dag_title = "Twitter Stream Temaplte"
    dag_text = "..."
    dag_footer = "..."
    pg_command = """INSERT INTO dag_dag ( id, track, type, title, text, footer) VALUES ( %s, %s, %s, %s, %s, %s )"""
    pg_hook.run(pg_command, parameters=[new_id, dag_track, dag_type, dag_title, dag_text, dag_footer])

    # Return the updated id name
    return new_id

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

schedule_interval = timedelta(days=365)

dag = DAG(
    dag_name,
    description="Simple template for DAGs that use the Twitter Streaming APIs",
    schedule_interval=schedule_interval,
    start_date=datetime.now(),
    concurrency=2,
    catchup=False)

# Setup the operators of the DAG
first_operator = PythonOperator(
    task_id="setupdb_task_01",
    python_callable=setup_db,
    provide_context=True,
    dag=dag)

second_operator = BashOperator(
    task_id="twitter-streams_task_02",
    bash_command="python /usr/local/airflow/dags/twitter-stream.py" + " --id="
    + "{{ ti.xcom_pull('setupdb_task_01') }}",
    retries=0,
    dag=dag)

# Setup the flow of operators in the DAG
first_operator >> second_operator
