import json
import os

from requests import request
from web3 import Web3
from web3.middleware.geth_poa import geth_poa_middleware

URL = os.environ.get("NODE_API_URL")

w3_client = Web3(Web3.HTTPProvider(endpoint_uri=URL))
w3_client.middleware_onion.inject(geth_poa_middleware, layer=0)

# print(w3_client.eth.get_block(12911679))

payload = json.dumps(
    {
        "method": "eth_blockNumber",
        "params": [],
        "id": 1,
        "jsonrpc": "2.0",
    }
)

# payload = json.dumps(
#     {
#         "method": "eth_getBlockByNumber",
#         "params": [
#             "0xc5043f",
#             False,
#         ],
#         "id": 1,
#         "jsonrpc": "2.0",
#     }
# )
response = request(
    "POST", URL, headers={"Content-Type": "application/json"}, data=payload
)
print(response.json())
# print(response.json()["result"])
