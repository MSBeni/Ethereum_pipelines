import pandas as pd

"""
bigquery.SchemaField("hash_", "STRING"),
bigquery.SchemaField("nonce", "STRING"),
bigquery.SchemaField("block_hash", "STRING"),
bigquery.SchemaField("block_number", "INTEGER"),
bigquery.SchemaField("transaction_index", "INTEGER"),
bigquery.SchemaField("from_address", "STRING"),
bigquery.SchemaField("to_address", "STRING"),
bigquery.SchemaField("value", "DECIMAL"),
bigquery.SchemaField("gas", "INTEGER"),
bigquery.SchemaField("gas_price", "INTEGER"),
bigquery.SchemaField("input", "INTEGER"),
bigquery.SchemaField("block_timestamp", "INTEGER"),
bigquery.SchemaField("max_fee_per_gas", "INTEGER"),
bigquery.SchemaField("max_priority_fee_per_gas", "INTEGER"),
bigquery.SchemaField("transaction_type", "INTEGER"),"""

df = pd.read_csv('transactions.csv')

# print(df.head(1))
#
# print(df.columns, len(list(df.columns)))
#
# print(type(df.block_timestamp[1]))
# print(type(df.max_priority_fee_per_gas[1]))

for col in list(df.columns):
    print(col, ": ", type(df[col][1]))