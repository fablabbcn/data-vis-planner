# -*- encoding: utf-8 -*-
#
# PostgreSQL to Mongo data export for the Meteor visualisations
#
# Author: Massimo Menichinelli
# E-mail: info@openp2pdesign.org - massimo@fablabbcn.org
# License: MIT
#
#

# Command line arguments
import sys
import getopt
# Work with time
from datetime import datetime
# Store and retrieve data in Mongo database
import mongoengine
# PostgreSQL hook from Airflow
from airflow.hooks.postgres_hook import PostgresHook
# Logging messages to Airflow
import logging


# Collections schemas using Mongoengine
# Documentation here: http://mongoengine.org/
# Document for the DAG as a whole
class DAG_Description(mongoengine.Document):
    dag_name = mongoengine.StringField(required=True, max_length=200)
    raw_data = mongoengine.DictField()
    clean_data = mongoengine.DictField()
    vis_type = mongoengine.StringField(required=True, max_length=200)
    vis_title = mongoengine.StringField(max_length=120)
    vis_configuration = mongoengine.StringField(max_length=400)
    vis_text = mongoengine.StringField(max_length=400)
    vis_footer = mongoengine.StringField(max_length=400)
    created_at = mongoengine.DateTimeField()
    updated_at = mongoengine.DateTimeField(default=datetime.now)
    meta = {"collection": "dags"}


# This function parses the command line argument and handle data accordingly
def cli(args):
    try:
        opts, args = getopt.getopt(args, "i:", ["id=", ])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('A simple script for loading data from PostgreSQL to Mongo')
            sys.exit()
        elif opt in ("-i", "--id"):
            row_id = arg

            # Connection to the PostgreSQL, to be defined in the Airflow UI
            pg_hook = PostgresHook(postgres_conn_id="postgres_data")

            # Retrieve the data stored in PostgreSQL
            pg_command = """SELECT * FROM dag_dag WHERE id = %s"""
            data = pg_hook.get_records(pg_command, parameters=[row_id])

            # Connect to Mongo databases in the Docker compose
            mongoengine.connect(db="dags", host="mongo:27017", alias="default")

            # Search for existing documents with the same dag_name
            dags_docs = DAG_Description.objects(dag_name="hello_world_template")

            # logging.info(type(dags_docs))
            # logging.info(dags_docs)

            # If there are no documents
            if len(dags_docs) == 0:
                # Setup a new document for storing the data
                logging.info("Creating a new Mongo document for %s", row_id)
                dag_document = DAG_Description(
                    dag_name=row_id,
                    raw_data=data[0][1],
                    clean_data=data[0][2],
                    vis_type=data[0][3],
                    vis_title=data[0][4],
                    vis_configuration=data[0][5],
                    vis_text=data[0][6],
                    vis_footer=data[0][7],
                    created_at=data[0][8],
                    updated_at=data[0][9])
                # Save the document
                dag_document.save()
            # If there are more than one documents, get the first one
            elif len(dags_docs) > 1:
                logging.info("Updating the first Mongo document found for %s", row_id)
                dag_document = dags_docs.first()
                dag_document.update(raw_data=data[0][1], clean_data=data[0][2], updated_at=datetime.now)
            # If there is only one document
            elif len(dags_docs) == 1:
                logging.info("Updating the Mongo document found for %s", row_id)
                dag_document = dags_docs.first()
                dag_document.update(raw_data=data[0][1], clean_data=data[0][2], updated_at=datetime.now)

            # Return the success message
            logging.info("Data exported from PostgreSQL to Mongo successfully.")


if __name__ == '__main__':
    cli(sys.argv[1:])
