SELECT DATE, STORE_LOCATION, ROUND((SUM(SP) - SUM(CP)), 2) AS lc_profit FROM clean_store_transactions
WHERE DATE = SUBDATE(date(now()),1) GROUP BY STORE_LOCATION ORDER BY lc_profit DESC
INTO OUTFILE '/var/lib/mysql-files/location_wise_profit_1.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
SELECT DATE, STORE_ID, ROUND((SUM(SP) - SUM(CP)), 2) AS st_profit FROM clean_store_transactions
WHERE DATE = SUBDATE(date(now()),1) GROUP BY STORE_ID ORDER BY st_profit DESC
INTO OUTFILE '/var/lib/mysql-files/store_wise_profit_1.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';
