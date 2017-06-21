import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'admin'
user.email = 'admin@example.com'
user.password = 'pass'
session = settings.Session()
session.add(user)
user.username = 'test'
user.email = 'test@example.com'
user.password = 'pass'
session.add(user)
session.commit()
session.close()
