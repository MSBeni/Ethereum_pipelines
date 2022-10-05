from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import pandas as pd
import matplotlib.pyplot as plt


credentials = json.loads(open("../../infuraApp.json", 'r').read())

infura_url = credentials['auth']['ENDPOINTS']

web3 = Web3(Web3.HTTPProvider(infura_url))


test_address = '0x8aecDAC523Eb208805780271BEBF19727F2f666F'

print("isConnected:", web3.isConnected())

latestBlock = web3.eth.getBlock(15669699)
print("Latest Block: ", latestBlock.size)
print("Latest Block: ", len(latestBlock.transactions))

average_trans_size = list()
blocknumber = list()
for transaction in range(15668000, 15669700):
    currentBlock = web3.eth.getBlock(transaction)
    try:
        average_trans_size.append(currentBlock.size/len(currentBlock.transactions))
        blocknumber.append(transaction)
    except:
        pass

df = pd.DataFrame()
df['block_number'] = blocknumber
df['Ave._Transaction_Size'] = average_trans_size
df.to_csv('trans_ave_size_3.csv')
plt.plot(blocknumber, average_trans_size)
print(average_trans_size)
plt.show()