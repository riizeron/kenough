from src.configs.config import postgres_config

from src.db.connectors.postgres_connector import PostgresConnector
from src.db.clients.postgres_client import PostgresClient
from src.db.repositories.sast_repository import SASTRepository


sast_repository = SASTRepository(
    db_client=PostgresClient(
        connector=PostgresConnector(
            db_url=f"postgresql+asyncpg://{postgres_config.username}:{postgres_config.password}"
                   f"@{postgres_config.host}:{postgres_config.port}/{postgres_config.database}"
        )
    )
)