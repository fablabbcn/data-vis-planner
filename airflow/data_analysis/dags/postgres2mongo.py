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
    title = mongoengine.StringField(max_length=120)
    vis_text = mongoengine.StringField(max_length=400)
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

            # Setup the document for storing the data
            dag_document = DAG_Description(
                dag_name=row_id,
                raw_data=data[0][1],
                clean_data=data[0][2],
                vis_type=str(data[0][3]),
                vis_title=str(data[0][4]),
                vis_text=str(data[0][5]))

            # Save the document
            dag_document.save()

            # Return the success message
            logging.info("Data exporte from PostgreSQL to Mongo successfully.")


if __name__ == '__main__':
    cli(sys.argv[1:])
