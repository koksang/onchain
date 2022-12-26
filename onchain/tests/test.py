import ray
from google.cloud import bigquery

bq = bigquery.Client()
print(bq.__dict__)

ray.init(address="ray://127.0.0.1:10001")

# # ray.init(address="auto")

# # ray.init()

print(ray.cluster_resources())
