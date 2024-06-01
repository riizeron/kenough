from src.configs.postgres_config import PostgresConfig
from src.configs.tool_config import ToolConfig

from src.utils.wait import wait_secret

class ReadData:
    """"""

    def __init__(self, config: dict):
        """"""

        self.config = config
        self.creds = config["secrets"]

        for path in tuple(self.creds["postgres"].values()) + tuple(self.creds["bb-http"].values()):
            wait_secret(path)

    def get_postgres_config(self) -> PostgresConfig:
        """Read database secrets"""

        db_host = self.config["db"]["host"]
        db_port = self.config["db"]["port"]
        db_database = self.config["db"]["database"]

        with open(self.creds["postgres"]["username-admin"]) as f:
            db_user = f.readline().rstrip()
        with open(self.creds["postgres"]["password-admin"]) as f:
            db_password = f.readline().rstrip()

        return PostgresConfig(db_user, db_password, db_host, db_port, db_database)


    def get_semgrep_config(self) -> ToolConfig:
        return ToolConfig(
            args=self.config["semgrep"]["args"],
            bin=self.config["semgrep"]["bin"],
            rule_path=self.config["semgrep"]["rule_path"],
            timeout=self.config["semgrep"]["timeout"],
            max_unpacked_size=self.config["semgrep"]["max_unpacked_size"]
        )
