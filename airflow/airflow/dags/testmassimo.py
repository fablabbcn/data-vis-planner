from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
#from airflow.models import Variable
import requests




def get_data():
    data = requests.get("https://api.fablabs.io/v0/labs.json").json()
    return data

#def give_feedback():
#    username = Variable.get("github_user")
#    return username


dag = DAG('hello_world', description='Simple tutorial DAG',
          schedule_interval='3 * * * *',
          start_date=datetime(2017, 3, 20), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

get_operator = PythonOperator(task_id='hello_task', python_callable=get_data, dag=dag)

#feedback_operator = PythonOperator(task_id='fdb_task', python_callable=give_feedback, dag=dag)

dummy_operator >> get_operator #>> feedback_operator
