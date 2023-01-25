"""Constants"""

import os
from pathlib import Path

PROJECT_PATH = str(Path(__file__).parents[1])
SERVICES_PATH = str(Path(PROJECT_PATH, "onchain", "services"))
CONFIG_PATH = str(Path(PROJECT_PATH, "conf"))
CONFIG_NAME = "main"
GOOGLE_APPLICATION_CREDENTIALS_B64 = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS_B64", None
)

# sources
SOURCE_SEND_LIMIT = 10
