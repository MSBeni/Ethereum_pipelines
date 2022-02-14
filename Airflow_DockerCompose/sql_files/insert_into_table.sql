LOAD DATA INFILE '/var/lib/mysql-files/clean_store_transactions.csv' INTO TABLE clean_store_transactions
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;