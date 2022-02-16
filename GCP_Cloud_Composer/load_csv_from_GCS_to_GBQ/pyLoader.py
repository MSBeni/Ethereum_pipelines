from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# Set table_id to the ID of the table to create.
table_id = "avian-force-340302.eth_transaction.transactions"
"""
    hash_ STRING,
    nonce BIGINT,
    block_hash STRING,
    block_number BIGINT,
    transaction_index BIGINT,
    from_address STRING,
    to_address STRING,
    value DECIMAL,
    gas BIGINT,
    gas_price BIGINT,
    input STRING,
    block_timestamp INT64,
    max_fee_per_gas INT64,
    max_priority_fee_per_gas INT64,
    transaction_type INT64
"""
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("hash_", "STRING"),
        bigquery.SchemaField("nonce", "INTEGER"),
        bigquery.SchemaField("block_hash", "STRING"),
        bigquery.SchemaField("block_number", "INTEGER"),
        bigquery.SchemaField("transaction_index", "INTEGER"),
        bigquery.SchemaField("from_address", "STRING"),
        bigquery.SchemaField("to_address", "STRING"),
        bigquery.SchemaField("value", "STRING"),
        bigquery.SchemaField("gas", "INTEGER"),
        bigquery.SchemaField("gas_price", "INTEGER"),
        bigquery.SchemaField("input", "STRING"),
        bigquery.SchemaField("block_timestamp", "INTEGER"),
        bigquery.SchemaField("max_fee_per_gas", "FLOAT64"),
        bigquery.SchemaField("max_priority_fee_per_gas", "FLOAT64"),
        bigquery.SchemaField("transaction_type", "INTEGER"),
    ],
    skip_leading_rows=1,
    # The source format defaults to CSV, so the line below is optional.
    source_format=bigquery.SourceFormat.CSV,
)
uri = "gs://us-west1-eth-transactions-2168f060-bucket/transactions.csv"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
print("Loaded {} rows.".format(destination_table.num_rows))