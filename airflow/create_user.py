import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

user = PasswordUser(models.User())
user.username = 'admin'
user.email = 'admin@example.com'
user.password = 'pass'
session = settings.Session()

try:
    session.add(user)
    session.commit()
    session.close()
except:
    print "Error with adding the default admin user, user probably already existing."
