"""Constants"""

import os
from pathlib import Path


PROJECT_PATH = str(Path(__file__).parents[1])
SERVICES_PATH = str(Path(PROJECT_PATH, "onchain", "services"))
CONFIG_PATH = str(Path(PROJECT_PATH, "config"))
CONFIG_NAME = "main"
GOOGLE_APPLICATION_CREDENTIALS_B64 = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS_B64", None
)

# sources
SOURCE_SEND_LIMIT = 10

BASE_PATH_PROTO_PYMODEL = "onchain.models.blockchains"
DEFAULT_PULSAR_PROXY_IP = "pulsar://localhost:6650"
