'''
pip3 install apache-airflow[gcp]
'''
from airflow import models
from datetime import datetime, timedelta
# from airflow.operators.python import PythonOperator
from airflow.operators import python_operator
from google.cloud import bigquery
from web3 import Web3
import pandas as pd
from web3.middleware import geth_poa_middleware
import json
# Construct a BigQuery client object.
client = bigquery.Client()


def read_las_block_save_to_csv():
    credentials = json.loads(open("../../infuraApp.json", 'r').read())
    infura_url = credentials['auth']['ENDPOINTS']
    web3 = Web3(Web3.HTTPProvider(infura_url))
    print("isConnected:", web3.isConnected())

    latestBlock = web3.eth.getBlock('latest')
    latest_transaction_df = pd.DataFrame()

    hash_ = []
    nonce = []
    block_hash = []
    block_number = []
    transaction_index = []
    from_address = []
    to_address = []
    value = []
    gas = []
    gas_price = []
    input = []
    block_timestamp = []
    max_fee_per_gas = []
    max_priority_fee_per_gas = []
    transaction_type = []

    # print(dict(web3.eth.get_transaction(dict(latestBlock)['transactions'][0])).keys())

    cols = ['hash', 'nonce', 'block_hash', 'block_number', 'transaction_index',
                                          'from_address', 'to_address', 'gas', 'gas_price', 'input', 'block_timestamp',
                                          'max_fee_per_gas', 'max_priority_fee_per_gas', 'transaction_type']
    # list of all the lists
    lists = [hash_, nonce, block_hash, block_number, transaction_index, from_address, to_address, value, gas, gas_price,
    input, block_timestamp, max_fee_per_gas, max_priority_fee_per_gas, transaction_type]

    for transaction in dict(latestBlock)['transactions']:
        trans = web3.eth.get_transaction(transaction)
        transDict = dict(trans)
        for i in range(len(lists)):
            try:
                lists[i].append(transDict[cols[i]])
            except:
                lists[i].append(None)


    latest_transaction_df['hash'] = hash_
    latest_transaction_df['nonce'] = nonce
    latest_transaction_df['block_hash'] = block_hash
    latest_transaction_df['block_number'] = block_number
    latest_transaction_df['transaction_index'] = transaction_index
    latest_transaction_df['from_address'] = from_address
    latest_transaction_df['to_address'] = to_address
    latest_transaction_df['gas'] = gas
    latest_transaction_df['gas_price'] = gas_price
    latest_transaction_df['input'] = input
    latest_transaction_df['block_timestamp'] = block_timestamp
    latest_transaction_df['max_fee_per_gas'] = max_fee_per_gas
    latest_transaction_df['max_priority_fee_per_gas'] = max_priority_fee_per_gas
    latest_transaction_df['transaction_type'] = transaction_type

    latest_transaction_df.to_csv('gs://us-west1-eth-transactions-2168f060-bucket/saved_data/latest_block_'
                                 + str(dict(latestBlock)['number']) + ".csv",
                                 columns=['hash', 'nonce', 'block_hash', 'block_number', 'transaction_index',
                                          'from_address', 'to_address', 'gas', 'gas_price', 'input', 'block_timestamp',
                                          'max_fee_per_gas', 'max_priority_fee_per_gas', 'transaction_type'])


def load_data():
    # Set table_id to the ID of the table to create.
    table_id = "avian-force-340302.eth_transaction.transactions2"
    """
        hash_ STRING,
        nonce BIGINT,
        block_hash STRING,
        block_number BIGINT,
        transaction_index BIGINT,
        from_address STRING,
        to_address STRING,
        value DECIMAL,
        gas BIGINT,
        gas_price BIGINT,
        input STRING,
        block_timestamp INT64,
        max_fee_per_gas INT64,
        max_priority_fee_per_gas INT64,
        transaction_type INT64
    """
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("hash_", "STRING"),
            bigquery.SchemaField("nonce", "INTEGER"),
            bigquery.SchemaField("block_hash", "STRING"),
            bigquery.SchemaField("block_number", "INTEGER"),
            bigquery.SchemaField("transaction_index", "INTEGER"),
            bigquery.SchemaField("from_address", "STRING"),
            bigquery.SchemaField("to_address", "STRING"),
            bigquery.SchemaField("value", "STRING"),
            bigquery.SchemaField("gas", "INTEGER"),
            bigquery.SchemaField("gas_price", "INTEGER"),
            bigquery.SchemaField("input", "STRING"),
            bigquery.SchemaField("block_timestamp", "INTEGER"),
            bigquery.SchemaField("max_fee_per_gas", "FLOAT64"),
            bigquery.SchemaField("max_priority_fee_per_gas", "FLOAT64"),
            bigquery.SchemaField("transaction_type", "INTEGER"),
        ],
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = "gs://us-west1-eth-transactions-2168f060-bucket/transactions.csv"

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))


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
    t1 = python_operator.PythonOperator(
        task_id='ethtask',
        python_callable=load_data,
        # options={'input': 'gs://daily_food_orders/food_daily.csv'}
    )
