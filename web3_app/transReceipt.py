from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import pprint

credentials = json.loads(open("../../infuraApp.json", 'r').read())

infura_url = credentials['auth']['ENDPOINTS']

web3 = Web3(Web3.HTTPProvider(infura_url))


transaction = '0xa80089f625861f3392075f12cdf223003d6540566dcf9293a643e27a6a9dec14'

print("isConnected:", web3.isConnected())

trans = web3.eth.get_transaction_receipt(transaction)
pp = pprint.PrettyPrinter(indent=4)
# print("Transaction info: ", trans)
pp.pprint(trans)