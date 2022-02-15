from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

credentials = json.loads(open("../../infuraApp.json", 'r').read())

infura_url = credentials['auth']['ENDPOINTS']

web3 = Web3(Web3.HTTPProvider(infura_url))


test_address = '0x8aecDAC523Eb208805780271BEBF19727F2f666F'

print("isConnected:", web3.isConnected())

latestBlock = web3.eth.getBlock(14212927)
print("Latest Block: ", latestBlock)