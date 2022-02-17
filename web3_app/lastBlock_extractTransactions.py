from web3 import Web3
import pandas as pd
from web3.middleware import geth_poa_middleware
import json
import pprint

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

latest_transaction_df.to_csv('latest_block_' + str(dict(latestBlock)['number']) + ".csv",
                             columns=['hash', 'nonce', 'block_hash', 'block_number', 'transaction_index',
                                      'from_address', 'to_address', 'gas', 'gas_price', 'input', 'block_timestamp',
                                      'max_fee_per_gas', 'max_priority_fee_per_gas', 'transaction_type'])
