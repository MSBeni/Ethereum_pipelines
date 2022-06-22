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


#
def query_stackoverflow(df, table_id):
    """
    hash :  <class 'str'>
    nonce :  <class 'numpy.int64'>
    block_hash :  <class 'str'>
    block_number :  <class 'numpy.int64'>
    transaction_index :  <class 'numpy.int64'>
    from_address :  <class 'str'>
    to_address :  <class 'str'>
    value :  <class 'str'>
    gas :  <class 'numpy.int64'>
    gas_price :  <class 'numpy.int64'>
    input :  <class 'str'>
    block_timestamp :  <class 'numpy.int64'>
    max_fee_per_gas :  <class 'numpy.float64'>
    max_priority_fee_per_gas :  <class 'numpy.float64'>
    transaction_type :  <class 'numpy.int64'>
    :param df:
    :param table_id:
    :param service_account_json:
    :return:
    """
    # construct a bigquery client object
    # client = bigquery.Client.from_service_account_json(service_account_json)
    client = bigquery.Client()
    # TODO(developer): Set table_id to the ID of table to append to.
    rows_to_insert = []
    for i in range(len(df.hash)):
        row_to_insert_ = {u"hash_": df['hash'][i], u"nonce": int(df['nonce'][i]),
                          u"block_hash": df['block_hash'][i], u"block_number": int(df['block_number'][i]),
                          u"transaction_index": int(df['transaction_index'][i]),
                          u"from_address": df['from_address'][i], u"to_address": df['to_address'][i],
                          u"value": df['value'][i],
                          u"gas": int(df['gas'][i]), u"gas_price": int(df['gas_price'][i]),
                          u"input": df['input'][i], u"block_timestamp": int(df['block_timestamp'][i]),
                          u"max_fee_per_gas": df['max_fee_per_gas'][i],
                          u"max_priority_fee_per_gas": df['max_priority_fee_per_gas'][i],
                          u"transaction_type": int(df['transaction_type'][i])}
        if row_to_insert_ not in rows_to_insert:
            rows_to_insert.append(row_to_insert_)

    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    if not errors:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

def read_las_block_save_to_csv(**kwargs):
    # credentials = json.loads(open("gs://us-west1-eth-transactions-2168f060-bucket/saved_data/infuraApp.json", 'r').read())
    # infura_url = credentials['auth']['ENDPOINTS']
    infura_url = 'https://mainnet.infura.io/v3/b12f5367873a4468b621a5f63cb74e39'
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
        try:
            trans = web3.eth.get_transaction(transaction)
            transDict = dict(trans)
            for i in range(len(lists)):
                try:
                    lists[i].append(transDict[cols[i]])
                except:
                    lists[i].append(None)
        except:
            print("Transaction with hash {} is not found".format(transaction))


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

    table_id = kwargs['table_id']
    # GCP_service_account_filepath = kwargs['GCP_service_account_filepath']
    # query_stackoverflow(latest_transaction_df, table_id, GCP_service_account_filepath)
    query_stackoverflow(latest_transaction_df, table_id)
    # latest_transaction_df.to_csv('gs://us-west1-eth-transactions-2168f060-bucket/saved_data/latest_block_'
    #                              + str(dict(latestBlock)['number']) + ".csv",
    #                              columns=['hash', 'nonce', 'block_hash', 'block_number', 'transaction_index',
    #                                      'from_address', 'to_address', 'gas', 'gas_price', 'input', 'block_timestamp',
    #                                       'max_fee_per_gas', 'max_priority_fee_per_gas', 'transaction_type'])



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

with models.DAG('extract_transactions_dag',
                default_args=default_args,
                schedule_interval='@daily',
                catchup=False) as dag:
    t1 = python_operator.PythonOperator(
        task_id='extethtask',
        python_callable=read_las_block_save_to_csv,
        op_kwargs={'table_id': 'avian-force-340302.eth_transaction.transactions2'
            # ,
            #        'GCP_service_account_filepath':
            #            'gs://us-west1-eth-transactions-2168f060-bucket/saved_data/client_secret_farnoush_gcp.json'
                   }
    )
