from python_graphql_client import GraphqlClient
import time
import pandas as pd
import plotly.express as px


# Start the client with an endpoint.
client = GraphqlClient(endpoint="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")


class Calls:
    def QueryDB(self, skipnumber):
        query = """˛˛
      {pairs(first:1000, skip:%s){
         id
         reserveUSD
         reserveETH
         totalSupply
         token0Price
         token1Price
         reserve0
         reserve1
         token0{id, symbol, name, tradeVolume, totalLiquidity}
         token1{id, symbol, name, tradeVolume, totalLiquidity}}}""" % skipnumber
        return query


# As there is close to 20.000 tokens now when article is wrtitten am using range up to 21.000 as call is limited per 1000
my_list = [*range(1, 21000, 1000)]
print(my_list)

for each in my_list:
    try:
        # calls queryDB with wanted statement (it can be changed based on documentation at uniswap api or graphql sandbox)
        data = client.execute(query=Calls().QueryDB(each))

        # Extract details from gathered data.

        for token_details in data["data"]["pairs"]:
            id_ = token_details["id"]
            token0Price = token_details["token0Price"]
            token1Price = token_details["token1Price"]
            reserveUSD = token_details["reserveUSD"]
            reserveETH = token_details["reserveETH"]
            reserve0 = token_details["reserve0"]
            reserve1 = token_details["reserve1"]

            # Time limit between calls - to avoid ban
            time.sleep(10)

    except:
        pass


# query = gql('''
#         query {
#         pairs (first: 10, where: {volumeUSD_gt: "10000000"})
#         {
#         volumeUSD
#         token0 {
#             symbol
#         }
#         token1 {
#             symbol
#         }
#         }
#         }
#     ''')
# response = client.execute(query)
# print(response)