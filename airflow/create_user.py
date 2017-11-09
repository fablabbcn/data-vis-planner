# Create a user for Airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

# Get configuration from the environment.env file
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../environment.env')
load_dotenv(dotenv_path)

# Create the user
user = PasswordUser(models.User())
user.username = os.environ.get("AIRFLOW_ADMIN")
user.email = os.environ.get("AIRFLOW_EMAIL")
user.password = os.environ.get("AIRFLOW_PASSWORD")
session = settings.Session()

try:
    session.add(user)
    session.commit()
    session.close()
except:
    print "Error with adding the default admin user, user probably already existing."
