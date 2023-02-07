from abc import ABC, abstractmethod
from psycopg2.extensions import connection
from contextlib import contextmanager

class AbstractConnectionManager(ABC):

    @abstractmethod
    def get_connection(self) -> connection:
        pass

    @abstractmethod
    def put_connection(self, connection: connection) -> None:
        pass


class ConnectionManager(AbstractConnectionManager):
    """
    Maybe this is a proxy, maybe an adapter. Who knows. It logs.
    """

    def __init__(self, name, get_connection, put_connection) -> None:
        self.name = name
        self._get_connection = get_connection
        self._put_connection = put_connection

    def get_connection(self) -> connection:
        conn = self._get_connection()
        print(f"get_connection on ConnectionManager({self.name}): {conn}")
        return conn

    def put_connection(self, connection: connection) -> None:
        print(
            f"put_connection on ConnectionManager({self.name}): {connection}")
        self._put_connection(connection)

    @contextmanager
    def cursor(self):
        try:
            conn = self.get_connection()
            with conn:
                yield conn.cursor()
        finally:
            self.put_connection(conn)
