"""BigQuery Source"""

from typing import Iterable
from google.cloud.bigquery import Client
from onchain.core.base import BaseSource
from onchain.core.logger import log
from onchain.utils.helpers import decode_b64_json_string
from onchain.constants import GOOGLE_APPLICATION_CREDENTIALS_B64


class BigQuerySource(BaseSource):
    def __init__(self, config: dict, **kwargs) -> None:
        """Init

        Args:
            config (dict): BigQuery sink config
        """
        self.config = config
        self.client = None
        log.info(f"Initiated {self._name} with config: {self.config}")

    def connect(self, reconnect: bool = False) -> None:
        """Establish client connection

        Args:
            reconnect (bool, optional): To reconnect the client?. Defaults to False.
        """
        # NOTE: Temporarily supporting GOOGLE_APPLICATION_CREDENTIALS or application default
        if not (self.client and reconnect) or reconnect:
            if GOOGLE_APPLICATION_CREDENTIALS_B64:
                credentials = decode_b64_json_string(GOOGLE_APPLICATION_CREDENTIALS_B64)
                self.client = Client(
                    credentials=credentials, project=self.config["project"]
                )
            else:
                self.client = Client()
            log.info("Connected to BigQuery client")

    def read(self, query: str) -> Iterable[str]:
        """Read from Bigquery

        Args:
            query (str): Query to compute / read
        """
        if not self.client:
            self.connect()

        # TODO: convert to protobuf schema
        for row in self.client.query(query).result():
            yield row.values()
