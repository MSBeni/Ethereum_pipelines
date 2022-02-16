CREATE TABLE IF NOT EXISTS  `avian-force-340302.eth_transaction.transactions` (
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

)