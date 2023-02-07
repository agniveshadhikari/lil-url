from psycopg2.pool import ThreadedConnectionPool
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .redirect_service import RedirectService
from .user_service import UserService
from .session_service import SessionService
from .connection_manager import ConnectionManager

@dataclass
class PoolConfig:
    min_conns: int
    max_conns: int


@dataclass
class ConnectionConfig:
    db: str
    user: str
    password: str
    host: str

class DatabaseService:

    def __init__(self, poolConfig, connectionConfig) -> None:
        self.pool = ThreadedConnectionPool(
            minconn=poolConfig.min_conns,
            maxconn=poolConfig.max_conns,
            dbname=connectionConfig.db,
            user=connectionConfig.user,
            password=connectionConfig.password,
            host=connectionConfig.host,
            sslmode="require"
        )


        self.redirects = RedirectService(self._get_connection_manager('redirects'))
        self.users = UserService(self._get_connection_manager('users'))
        self.sessions = SessionService(
            self._get_connection_manager('sessions'))

    def _get_connection_manager(self, name):
        return ConnectionManager(name, self.pool.getconn, self.pool.putconn)
