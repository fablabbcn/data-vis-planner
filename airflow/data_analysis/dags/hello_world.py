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
# Load variables stored in Airflow
from airflow.models import Variable

# Work with time
from datetime import datetime

# Store and retrieve data in Mongo database
from pymongo import MongoClient

# Example: load data from Fablabs.io
from makerlabs import fablabs_io


# DAG name (for the DAG but also for the databases)
dag_name = "hello_world"

# Connect to Mongo database in the Docker compose
client = MongoClient('mongodb://mongo:27017')
# Create a database for this DAG
db = client[dag_name]
# Update the list of Meteor visualizations with this database
db_meteor_list = client['meteor_visualizations_list']


# Setup the Python functions for the operators

# This function loads data and saves it into the raw collection
def first_def():
    data = fablabs_io.get_labs(format="dict")
    # Save raw data in the raw collection
    db.raw.insert_one(data)
    return "Data saved successfully."

# This function loads raw data, transforms it for the visualization
# and update the list of visualizations in Meteor
def second_def():
    # Load data from the raw collection
    data = db.raw.find_one({})
    # Save meteor-ready data in the viz collection
    db.viz.insert_one(data)
    # Update the list of visualizations in Meteor
    meteor_viz = db_meteor_list.vizs.find_one({"name": dag_name})
    meteor_viz["type"] = "geo"
    db_meteor_list.vizs.insert_one(meteor_viz)
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
          description='Simple template for DAGs',
          schedule_interval='3 * * * *',
          start_date=datetime(2017, 3, 20),
          catchup=False)


# Setup the operators
first_operator = PythonOperator(
    task_id='hello_task_01',
    python_callable=first_def,
    dag=dag)

second_operator = PythonOperator(
    task_id='hello_task_02',
    python_callable=second_def,
    dag=dag)


# Setup the flow of operators
first_operator >> second_operator
