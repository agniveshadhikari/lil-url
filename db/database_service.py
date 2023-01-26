from psycopg2.pool import ThreadedConnectionPool

from .redirect_service import RedirectService


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

        self.redirects = RedirectService(self.pool.getconn, self.pool.putconn)
        # self.users = UserService()
        # self.sessions = SessionService()
