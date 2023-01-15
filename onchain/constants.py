"""Constants"""

from pathlib import Path

PROJECT_PATH = str(Path(__file__).parents[1])
SERVICES_PATH = str(Path(PROJECT_PATH, "onchain", "services"))
CONFIG_PATH = str(Path(PROJECT_PATH, "conf"))
CONFIG_NAME = "main"
