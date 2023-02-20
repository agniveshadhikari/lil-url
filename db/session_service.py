from .connection_manager import AbstractConnectionManager
from .model import User


class SessionService:
    def __init__(self, connection_manager: AbstractConnectionManager) -> None:
        self.connection_manager = connection_manager

    def create(self, token, user_id, expire_time):
        with self.connection_manager.cursor() as curs:
            curs.execute(
                """
                insert into session (token, user_id, expire_time)
                values(%s, %s, %s)
                """,
                (token, user_id, expire_time))

    def get_user(self, token) -> str:
        if token is None:
            return None
        with self.connection_manager.cursor() as curs:
            curs.execute(
                """
                select "user".id, username, first_name, middle_name, last_name, access_level, last_login_time
                from session join "user" on "user".id = session.user_id
                where token=%s
                    and expire_time >= CURRENT_TIMESTAMP
                """,
                (token,))

            result = curs.fetchone()
            if result is None:
                return None

            id, username, first_name, middle_name, last_name, access_level, last_login_time = result
            return User(id,
                        username=username,
                        first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                        access_level=access_level,
                        last_login_time=last_login_time)
