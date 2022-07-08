import requests
import json
from web3 import Web3
import urllib.request

# etherscanapikey = json.loads(open('../../etherscan_apiKey.json', 'r').read())
#
# # Obtaining a contract's ABI
# sc = requests.get('https://api-mainnet.etherscan.io/api?module=contract&action=getabi&address=0xc00e94Cb662C3520282E6f5717214004A7f26888&apikey=' + etherscanapikey['auth']['api_key'])
# abi = sc.json()
"""
ABI: Application Binary Interface allows anyone writing a smart contract to be able to communicate between a web 
application written in a high-level language like Javascript and the bytecode that the EVM understands
"""
compound_abi = json.loads(open('compound_abi.json', 'r').read())
address = '0xc00e94Cb662C3520282E6f5717214004A7f26888'

# Connecting to a node
"""
To interact with smart contracts, we will need a connection to an Ethereum node such as Infura, Alchemy or even running 
one of your own. We're using Infura in this case, make sure to set your endpoint to the Ropsten Testnet and copy the 
WebSockets (WSS) endpoint.
"""
credentials = json.loads(open("../../infuraApp.json", 'r').read())

infura_url = credentials['auth']['ENDPOINTS']

web3 = Web3(Web3.HTTPProvider(infura_url))
print(web3.isConnected())

contract = web3.eth.contract(address=address, abi=compound_abi)

# READ Data from Blockchain
totalSupply = contract.functions.totalSupply().call()
print(web3.fromWei(totalSupply, 'ether'))
print(contract.functions.name().call())
print(contract.functions.symbol().call())
print(contract.functions.balanceOf('0xfbe18f066F9583dAc19C88444BC2005c99881E56').call())