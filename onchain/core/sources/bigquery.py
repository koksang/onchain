"""BigQuery Source"""

from typing import Iterable, Union
from google.cloud.bigquery import Client
from onchain.core.base import BaseConnectionModule
from onchain.utils.helpers import decode_b64_json_string
from onchain.logger import log
from onchain.constants import GOOGLE_APPLICATION_CREDENTIALS_B64


class BigQuerySource(BaseConnectionModule):
    def __init__(
        self,
        client_config: dict,
        blockchain_name: str,
        blockchain_data: str,
        dbt_model: Union[str, None] = None,
        **kwargs,
    ) -> None:
        """Init

        Args:
            client_config (dict): BigQuery client configuration.
            blockchain_name (str): Blockchain name.
            blockchain_data (str): Blockchain data.
            dbt_model (str): Blockchain dbt model to run.
        """
        self._client_config = client_config
        self.dbt_model = dbt_model
        super().__init__(blockchain_name, blockchain_data)

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
                    credentials=credentials, project=self._client_config["project"]
                )
            else:
                self.client = Client()
            log.info("Connected to BigQuery client")

    def run(self) -> Iterable[str]:
        """Read from Bigquery"""
        if not self.client:
            self.connect()

        # TODO: convert to protobuf schema
        for row in self.client.query(self.dbt_model).result():
            yield row.values()
