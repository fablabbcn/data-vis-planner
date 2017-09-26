# -*- encoding: utf-8 -*-
#
# Twitter Stream to Mongo
#
# Author: Massimo Menichinelli
# E-mail: info@openp2pdesign.org - massimo@fablabbcn.org
# License: MIT
#
#

# Work with Twitter API
import twitter
# Work with JSON data
import json
import jsonpickle
# Store and retrieve data in Mongo database
import mongoengine
# Command line arguments
import sys
import getopt
# Work with time
from datetime import datetime
# Load variables stored in Airflow
# for passwords, access to databases, API keys and so on...
from airflow.models import Variable
# PostgreSQL hook from Airflow
from airflow.hooks.postgres_hook import PostgresHook
# Logging messages to Airflow
import logging


# Collections schemas using Mongoengine
# Documentation here: http://mongoengine.org/
# Document for the Twitter stream
class Twitter_Stream(mongoengine.Document):
    dag_name = mongoengine.StringField(required=True, max_length=200)
    twitter_query = mongoengine.StringField()
    raw_data = mongoengine.ListField(mongoengine.DictField())
    vis_type = mongoengine.StringField(required=True, max_length=200)
    vis_title = mongoengine.StringField(max_length=120)
    vis_text = mongoengine.StringField(max_length=400)
    updated_at = mongoengine.DateTimeField(default=datetime.now)
    meta = {"collection": "twitter_stream"}


# This function parses the command line argument and handle data accordingly
def cli(args):
    try:
        opts, args = getopt.getopt(args, "i:", ["id=", ])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'A simple script for listening to the Twitter Stream APIs and saving the data to Mongo')
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

            # Twitter API variables
            # Get them from http://dev.twitter.com

            # Add this variable in the admin UI: twitter_api
            # {"oauth_token": "xxx", "oauth_secret": "xxx", "consumer_key": "xxx", "consumer_secret": "xxx"}

            # Get Twitter API credentials from Airflow variable
            twitter_api = Variable.get("twitter_api", deserialize_json=True)

            OAUTH_TOKEN = twitter_api['oauth_token']
            OAUTH_SECRET = twitter_api['oauth_secret']
            CONSUMER_KEY = twitter_api['consumer_key']
            CONSUMER_SECRET = twitter_api['consumer_secret']

            # Start receiving tweets from the Twitter Stream API
            twitter_stream = twitter.TwitterStream(auth=twitter.OAuth(
                OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

            # Filter the Twitter Stream
            iterator = twitter_stream.statuses.filter(track=str(data[0][1]))

            # The task ends only manually, so we just log this message
            logging.info("Twitter Stream started successfully.")

            # Iterate over the stream of tweets
            for num, tweet in enumerate(iterator):

                json_object = jsonpickle.encode(tweet)

                json_dict = json.loads(json_object)

                logging.info("Tweet saved in the database.")

                if num == 0:
                    # Setup the document for storing the data
                    dag_document = Twitter_Stream(
                        dag_name=row_id,
                        raw_data=[json_dict],
                        vis_type=str(data[0][2]),
                        vis_title=str(data[0][3]),
                        vis_text=str(data[0][4]))
                    # Create the document
                    dag_document.save()

                else:
                    # Update the document
                    dag_document.update(add_to_set__raw_data=[json_dict])


if __name__ == '__main__':
    cli(sys.argv[1:])
