import json
import sys

import clickhouse_connect

CLICKHOUSE_CLOUD_HOSTNAME = "localhost"
CLICKHOUSE_CLOUD_USER = "onchain"
CLICKHOUSE_CLOUD_PASSWORD = "onchain"
CLICKHOUSE_PORT = 8123

client = clickhouse_connect.get_client(
    # interface="http",
    host=CLICKHOUSE_CLOUD_HOSTNAME,
    port=CLICKHOUSE_PORT,
    username=CLICKHOUSE_CLOUD_USER,
    password=CLICKHOUSE_CLOUD_PASSWORD,
)

print("connected to " + CLICKHOUSE_CLOUD_HOSTNAME + "\n")

client.command(
    "CREATE TABLE IF NOT EXISTS test_table (key UInt32, value String, metric Float64) ENGINE MergeTree ORDER BY key"
)

print("table test_table created or exists already!\n")

row1 = [1000, "String Value 1000", 5.233]
row2 = [2000, "String Value 2000", -107.04]
data = [row1, row2]
client.insert("test_table", data, column_names=["key", "value", "metric"])

print("written 2 rows to table test_table\n")

QUERY = "SELECT max(key), avg(metric) FROM test_table"

result = client.query(QUERY)

sys.stdout.write("query: [" + QUERY + "] returns:\n\n")
print(result.result_rows)
