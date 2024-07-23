"""Dbt runner"""

import subprocess
from onchain.logger import log


class DbtRunner:
    def __init__(self, target: str = "default", **kwargs) -> None:
        """Initialize DBT model runner

        Args:
            target (str, optional): DBT target profile. Defaults to "default".
        """
        self.target = target
        log.info(f"Initiated DBT runner - target: {self.target}")

    def run(self, model: str, *args) -> None:
        """Run dbt model

        Args:
            model (str): DBT model name
        """
        cmd = ["dbt", "run", "-m", model, "-t", self.target, *args]
        try:
            output = subprocess.run(
                cmd, check=True, capture_output=True, encoding="utf-8"
            )
            log.info(f"Successful DBT run: {' '.join(output.args)}")
        except subprocess.CalledProcessError:
            log.error(f"Failed to run: {' '.join(output.args)}")
            log.error(output.stdout)
