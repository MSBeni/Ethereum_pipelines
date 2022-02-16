import pandas as pd


df = pd.read_csv('transactions.csv')

print(df.head(1))

print(df.columns, len(list(df.columns)))

print(type(df.block_timestamp[1]))
print(type(df.max_priority_fee_per_gas[1]))