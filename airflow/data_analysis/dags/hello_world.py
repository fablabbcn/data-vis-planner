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
from mongoengine import *

# Example: load data from Fablabs.io
from makerlabs import fablabs_io


# DAG name (for the DAG but also for the database)
dag_name = "hello_world"


# Connect to Mongo databases in the Docker compose
# Database for this DAG
connect(db=dag_name, host="mongodb://mongo:27017", alias="dag")
# Database for the Meteor visualizations settings
connect(db="meteor_visualizations_list", host="mongodb://mongo:27017", alias="viz")


# Collections schemas, using Mongoengine

# Document for raw data
class Raw(Document):
    title = StringField(required=True, max_length=200)
    data = DictField(required=True)
    published = DateTimeField(default=datetime.now)
    meta = {"db_alias": "dag", "collection": "raw"}

# Document for data cleaned for Meteor
class Clean(Document):
    title = StringField(required=True, max_length=200)
    data = DictField(required=True)
    published = DateTimeField(default=datetime.now)
    meta = {"db_alias": "dag", "collection": "clean"}

# Document for settings of the Meteor visualization
class Viz(Document):
    title = StringField(required=True, max_length=200)
    published = DateTimeField(default=datetime.now)
    clean_data = ReferenceField(Clean)
    raw_data = ReferenceField(Clean)
    meta = {"db_alias": "viz", "collection": "meteor_viz"}


# Setup the Python functions for the operators

# This function loads data and saves it into the raw collection
def first_def():
    # Get raw data from Fablabs.io, as an example
    data = fablabs_io.get_labs(format="dict")
    # Save raw data in the raw collection
    raw_content = Raw(
    title=dag_name+"_raw",
    data=data
    )
    raw_content.save()
    return "Data saved successfully."

# This function loads raw data, transforms it for the visualization
# and update the list of visualizations in Meteor
def second_def():
    # Load data from the raw collection
    data = Raw.objects(title=dag_name+"_raw")[0]
    # Clean the data for Meteor
    clean_content = Clean(
    title=dag_name+"_clean",
    data={"data":len(data)}
    )
    clean_content.save()
    # Save meteor-ready data in the viz collection
    # db.viz.insert_one(data)
    # Update the list of visualizations in Meteor
    meteor_viz = Viz(
    title=dag_name+"_meteor",
    raw_data=data.id,
    clean_data=clean_content.id
    )
    meteor_viz.save()
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
          schedule_interval="3 * * * *",
          start_date=datetime(2017, 3, 20),
          catchup=False)


# Setup the operators
first_operator = PythonOperator(
    task_id="hello_task_01",
    python_callable=first_def,
    dag=dag)

second_operator = PythonOperator(
    task_id="hello_task_02",
    python_callable=second_def,
    dag=dag)


# Setup the flow of operators
first_operator >> second_operator
