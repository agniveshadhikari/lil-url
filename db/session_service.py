from .connection_manager import AbstractConnectionManager
from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    first_name: str
    middle_name: str
    last_name: str


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
                select "user".id, username, first_name, middle_name, last_name
                from session join "user" on "user".id = session.user_id
                where token=%s
                    and expire_time >= CURRENT_TIMESTAMP
                """,
                (token,))

            result = curs.fetchone()
            if result is None:
                return None

            id, username, first_name, middle_name, last_name = result
            return User(id, username, first_name, middle_name, last_name)
