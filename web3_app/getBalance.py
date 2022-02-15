from web3 import Web3
import json

credentials = json.loads(open("../../infuraApp.json", 'r').read())

infura_url = credentials['auth']['ENDPOINTS']

web3 = Web3(Web3.HTTPProvider(infura_url))


test_address = '0x8aecDAC523Eb208805780271BEBF19727F2f666F'

print("isConnected:", web3.isConnected())

balance = web3.eth.getBalance(test_address)
print("Balance: ", web3.fromWei(balance, "ether"))