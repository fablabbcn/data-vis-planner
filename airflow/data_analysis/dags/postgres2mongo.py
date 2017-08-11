# -*- encoding: utf-8 -*-
#
# Template for Airflow DAGS
#
# Author: Massimo Menichinelli
# E-mail: info@openp2pdesign.org - massimo@fablabbcn.org
# License: MIT
#
#


# Work with time
from datetime import datetime

# Store and retrieve data in Mongo database
from mongoengine import *


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


# This function loads data and saves it into the raw collection
def first_def():
    # global raw_content
    # Get raw data from Fablabs.io, as an example
    data = fablabs_io.get_labs(format="dict")
    # Save raw data in the raw collection
    raw_content.data = data
    raw_content.save()
    return "Data saved successfully."


# This function loads raw data, transforms it for the visualization
def second_def():
    global raw_content
    global clean_content
    # Load data from the raw collection
    data = raw_content.data
    # Clean the data for the Meteor visualisation
    clean_content.data = {"data": len(data)}
    clean_content.save()
    return "Data prepared for the visualization successfully."


# This function updates the list of visualizations in Meteor
def third_def():
    global clean_content
    global meteor_content
    # Load data from the clean collection
    data = clean_content.data
    # Update the list of visualizations in Meteor
    meteor_content.data = data
    meteor_content.vis_type = "barchart"
    meteor_content.save()
    return "Data prepared for the visualization successfully."


raw_content.data = {"data": "testing save functionality with mongodb"}
raw_content.save()
