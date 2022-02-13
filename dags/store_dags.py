from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta
from datacleaner import data_cleaner

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2022, 2, 13),
    "email": ["airflow@airflow.com"],
    "retries": 1,
    "retry_delay": timedelta(seconds=5),
}

yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')


with DAG('store_dag', default_args=default_args, schedule_interval='@daily',
         template_searchpath=['/usr/local/airflow/sql_files'], catchup=False) as dag:

    t1 = BashOperator(task_id='check_file_availability',
                      bash_command='shasum ~/store_files_airflow/raw_store_transactions.csv', retries=2,
                      retry_delay=timedelta(seconds=15))

    t2 = PythonOperator(task_id='clean_raw_csv', python_callable=data_cleaner)

    t3 = MySqlOperator(task_id='create_mysql_table', mysql_conn_id="mysql_conn", sql="create_table.sql")

    t4 = MySqlOperator(task_id='insert_into_table', mysql_conn_id="mysql_conn", sql="insert_into_table.sql")

    t5 = MySqlOperator(task_id='select_from_table', mysql_conn_id="mysql_conn", sql="select_from_table.sql")


    t6 = BashOperator(task_id='move_file1', bash_command='cat ~/store_files_airflow/location_wise_profit_2.csv '
                                                         '&& mv ~/store_files_airflow/location_wise_profit_2.csv'
                                                         ' ~/store_files_airflow/location_wise_profit_2_%s.csv'
                                                         % yesterday_date)

    t7 = BashOperator(task_id='move_file2', bash_command='cat ~/store_files_airflow/store_wise_profit_2.csv '
                                                         '&& mv ~/store_files_airflow/store_wise_profit_2.csv'
                                                         ' ~/store_files_airflow/store_wise_profit_2_%s.csv'
                                                         % yesterday_date)

    t8 = EmailOperator(task_id='send_email',
        to='msbeni@gmail.com',
        subject='Daily report generated',
        html_content=""" <h1>Congratulations! Your store reports are ready.</h1> """,
        files=['/var/lib/mysql-files/location_wise_profit_2_%s.csv' % yesterday_date,
               '/var/lib/mysql-files/store_wise_profit_2_%s.csv' % yesterday_date])

    t9 = BashOperator(task_id='rename_raw',
                      bash_command='mv ~/var/lib/mysql-files/raw_store_transactions.csv'
                                   ' ~/var/lib/mysql-files/raw_store_transactions_%s.csv' % yesterday_date)


    t8 = EmailOperator(task_id='send_email',
        to='mohammad.salimi.b@gmail.com',
        subject='Daily report generated',
        html_content=""" <h1>Congratulations! Your store reports are ready.</h1> """,
        files=['/usr/local/airflow/store_files_airflow/location_wise_profit_%s.csv' % yesterday_date,
               '/usr/local/airflow/store_files_airflow/store_wise_profit_%s.csv' % yesterday_date])

    t9 = BashOperator(task_id='rename_raw',
                      bash_command='mv ~/store_files_airflow/raw_store_transactions.csv'
                                   ' ~/store_files_airflow/raw_store_transactions_%s.csv' % yesterday_date)

    t1 >> t2 >> t3 >> t4 >> t5 >> [t6, t7] >> t8 >> t9
