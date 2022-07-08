# Instanciate the protocol with the name, version and chain
from deficrawler import Lending

aave = Lending(protocol="Aave", chain="Ethereum", version=2)
aave_polygon = Lending(protocol="Aave", chain="Polygon", version=2)
compound = Lending(protocol="Compound", chain="Ethereum", version=2)
cream = Lending(protocol="Cream", chain="Ethereum", version=2)
cream_bsc = Lending(protocol="Cream", chain="bsc", version=2)

# Not all the protocols has the same available events to get data, to know which entities are supported for each protocol:
aave.supported_entities()
# uniswap.suported_entities()

# For each different entity, data can be retrieved in a specific time range.
print(compound.get_data_from_date_range('05/05/2022 10:20:20', '05/05/2022 10:40:20', "borrow"))

# To get the all the users of a protocol

print(cream_bsc.get_all_users())

# And the user positions
# print(cream_bsc.get_all_users(user))
print(cream_bsc.get_user_positions(user='0xfc0626831c5e8c3e888211bf08d02466415ca8b0'))