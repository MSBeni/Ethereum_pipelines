from python_graphql_client import GraphqlClient
import time
import pandas as pd
import plotly.express as px

client = GraphqlClient(endpoint="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")

query = ('''
        query {
        pairs (first: 10, where: {volumeUSD_gt: "100000"})
        {
        volumeUSD
        token0 {
            symbol
        }
        token1 {
            symbol
        }
        }
        }
    ''')
data = client.execute(query=query)
# print(data)

pairs = list()
for pr in data['data']['pairs']:
    pairs.append([
        pr['token0']['symbol'],
        pr['token1']['symbol'],
        pr['volumeUSD']
    ])

df = pd.DataFrame(pairs, columns=['Token 1', 'Token 2', 'Volume-USD'])
df['Volume-USD'] = df['Volume-USD'].astype(float)
df['Pair'] = df['Token 1'] + '-' + df['Token 2']
fig = px.bar(df, x='Pair', y='Volume-USD')
fig.show()