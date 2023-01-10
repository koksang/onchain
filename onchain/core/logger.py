"""Logger module"""

import sys
from loguru import logger as log

FORMAT = "{time:YYYY-MM-DD HH:mm} [{level: ^9}] {name}.{function}.{line} - {message}"
log.remove(0)
log.add(sys.stderr, format=FORMAT, colorize=True, level="INFO")
