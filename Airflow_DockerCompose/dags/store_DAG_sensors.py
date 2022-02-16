from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.email_operator import EmailOperator
from airflow.contrib.sensors.file_sensor import FileSensor

from datacleaner import data_cleaner

yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2022, 2, 13),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('store_dag', default_args=default_args, schedule_interval='@daily',
         template_searchpath=['/usr/local/airflow/sql_files'], catchup=True) as dag:

    # t1=BashOperator(task_id='check_file_exists', bash_command='shasum ~/store_files_airflow/
    # raw_store_transactions.csv', retries=2, retry_delay=timedelta(seconds=15))

    t1 = FileSensor(
        task_id='check_file_exists',
        filepath='/usr/local/airflow/store_files_airflow/raw_store_transactions.csv',
        fs_conn_id='fs_default',
        poke_interval=10,
        timeout=150,
        soft_fail=True
    )

    t2 = PythonOperator(task_id='clean_raw_csv', python_callable=data_cleaner)

    t3 = MySqlOperator(task_id='create_mysql_table', mysql_conn_id="mysql_conn", sql="create_table.sql")

    t4 = MySqlOperator(task_id='insert_into_table', mysql_conn_id="mysql_conn", sql="insert_into_table.sql")

    t5 = MySqlOperator(task_id='select_from_table', mysql_conn_id="mysql_conn", sql="select_from_table.sql")

    t6 = BashOperator(task_id='move_file1', bash_command='cat ~/store_files_airflow/location_wise_profit.csv && mv'
                                                         ' ~/store_files_airflow/location_wise_profit.csv'
                                                         ' ~/store_files_airflow/location_wise_profit_%s.csv'
                                                         % yesterday_date)

    t7 = BashOperator(task_id='move_file2', bash_command='cat ~/store_files_airflow/store_wise_profit.csv && mv'
                                                         ' ~/store_files_airflow/store_wise_profit.csv'
                                                         ' ~/store_files_airflow/store_wise_profit_%s.csv'
                                                         % yesterday_date)

    t8 = EmailOperator(task_id='send_email',
        to='example@example.com',
        subject='Daily report generated',
        html_content=""" <h1>Congratulations! Your store reports are ready.</h1> """,
        files=['/usr/local/airflow/store_files_airflow/location_wise_profit_%s.csv' % yesterday_date,
               '/usr/local/airflow/store_files_airflow/store_wise_profit_%s.csv' % yesterday_date])

    t9 = BashOperator(task_id='rename_raw', bash_command='mv ~/store_files_airflow/raw_store_transactions.csv '
                                                         '~/store_files_airflow/raw_store_transactions_%s.csv'
                                                         % yesterday_date)

    t1 >> t2 >> t3 >> t4 >> t5 >> [t6, t7] >> t8 >> t9
