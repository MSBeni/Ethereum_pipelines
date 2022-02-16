from airflow import DAG

# gs://us-west1-eth-transactions-2168f060-bucket/pyLoader.py

'''
pip3 install apache-airflow[gcp]
'''
from airflow import models
from datetime import datetime, timedelta
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2022, 2, 16),
    'retries': 0,
    'retry_delay': timedelta(seconds=50),
    'dataflow_default_options': {
        'project': 'avian-force-340302',
        'region': 'us-west1',
        'runner': 'DataflowRunner'
    }
}

with models.DAG('transactions_dag',
                default_args=default_args,
                schedule_interval='@daily',
                catchup=False) as dag:
    t1 = DataFlowPythonOperator(
        task_id='ethtask',
        py_file='gs://us-west1-eth-transactions-2168f060-bucket/pyLoader.py',
        # options={'input': 'gs://daily_food_orders/food_daily.csv'}
    )
