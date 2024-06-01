from src.db.abc.connector import Connector

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

import sqlalchemy


class PostgresConnector(Connector):
    """"""

    def __init__(self, db_url):
        """"""

        self.engine = create_async_engine(
            db_url,
            echo=False,
            connect_args={
                'prepared_statement_name_func': lambda: '',
                'statement_cache_size': 0,
            },
            poolclass=sqlalchemy.NullPool,
        )

        self.session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @property
    def get_session(self) -> sessionmaker[AsyncSession]:
        """"""

        return self.session

        # async with await self.engine.connect() as conn:
        #     return conn
