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
# for passwords, access to databases, API keys and so on...
from airflow.models import Variable
# You can load variables in this way:
# my_new_python_variable = Variable.get("variable_name_in_airflow_UI")

# Work with time
from datetime import datetime

# Store and retrieve data in Mongo database
from mongoengine import *

# Example: load data from Fablabs.io
from makerlabs import fablabs_io


# DAG name (for the DAG but also for the database)
dag_name = "hello_world"

# Connect to Mongo databases in the Docker compose
# Database for this DAG
connect(db="dags",
        host="mongo:27017",
        alias="default")


# Collections schemas, using Mongoengine
# Documentation here: http://mongoengine.org/

# Document for raw data
class Raw(Document):
    title = StringField(required=True, max_length=200)
    data = DictField()
    published = DateTimeField(default=datetime.now)
    meta = {"collection": "raw"}


# Document for data cleaned for Meteor
class Clean(Document):
    title = StringField(required=True, max_length=200)
    data = DictField()
    published = DateTimeField(default=datetime.now)
    meta = {"collection": "clean"}


# Document for settings of the Meteor visualization
class Vis(Document):
    title = StringField(required=True, max_length=200)
    published = DateTimeField(default=datetime.now)
    data = DictField()
    vis_type = StringField(required=True, max_length=200)
    meta = {"collection": "meteor"}


# Document for the DAG as a whole
class DAG_Description(Document):
    title = StringField(required=True, max_length=200)
    raw_data = ReferenceField(Raw)
    clean_data = ReferenceField(Clean)
    meteor_data = ReferenceField(Vis)
    published = DateTimeField(default=datetime.now)
    meta = {"collection": "dags"}


# Setup the collections for storing the data
# Collections are created here in order to be available to all defs
# Collection for raw data
raw_content = Raw(title=dag_name + "_raw")
raw_content.save()
# Collection for clean data
clean_content = Clean(title=dag_name + "_clean")
clean_content.save()
# Collection for Meteor data
meteor_content = Vis(title=dag_name + "_meteor",
                     vis_type="none")
meteor_content.save()
# Collection for DAG data
dag_document = DAG_Description(title=dag_name,
                               raw_data=raw_content,
                               clean_data=clean_content,
                               meteor_data=meteor_content)
dag_document.save()


# Setup the Python functions for the operators

# This function loads data and saves it into the raw collection
def first_def():
    # Get raw data from Fablabs.io, as an example
    data = fablabs_io.get_labs(format="dict")
    # Save raw data in the raw collection
    raw_content.data = data
    raw_content.save()
    return "Data saved successfully."


# This function loads raw data, transforms it for the visualization
def second_def():
    # Load data from the raw collection
    data = raw_content.data
    # Clean the data for the Meteor visualisation
    clean_content.data = {"data": len(data)}
    clean_content.save()
    return "Data prepared for the visualization successfully."


# This function updates the list of visualizations in Meteor
def third_def():
    # Load data from the clean collection
    data = clean_content.data
    # Update the list of visualizations in Meteor
    meteor_content.data = data
    meteor_content.vis_type = "barchart"
    meteor_content.save()
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
          schedule_interval="@once",
          start_date=datetime(2017, 3, 20),
          catchup=False)

# Setup the operators of the DAG
first_operator = PythonOperator(
    task_id="hello_task_01", python_callable=first_def, dag=dag)

second_operator = PythonOperator(
    task_id="hello_task_02", python_callable=second_def, dag=dag)

third_operator = PythonOperator(
    task_id="hello_task_03", python_callable=third_def, dag=dag)

# Setup the flow of operators in the DAG
first_operator >> second_operator >> third_operator
