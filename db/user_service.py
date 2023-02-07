from dataclasses import dataclass
import bcrypt

from .connection_manager import AbstractConnectionManager


@dataclass
class User:
    id: int
    username: str
    first_name: str
    middle_name: str
    last_name: str


class UserService:
    def __init__(self, connection_manager: AbstractConnectionManager) -> None:
        self.connection_manager = connection_manager

    # def create(self, username, password, first_name, middle_name, last_name):
    #     conn = self.connection_manager.get_connection()
    #     with conn.cursor() as curs:
    #         curs.execute(
    #             """
    #             insert into redirect (token, user_id, expire_time)
    #             values(%s, %s, %s)
    #             """,
    #             (token, user_id, expire_time))
    #     conn.commit()

    def authenticate(self, username, password) -> str:
        with self.connection_manager.cursor() as curs:
            curs.execute(
                """
                select password_hash, id
                from "user"
                where username=%s
                    and delete_time is NULL
                """,
                (username,))

            result = curs.fetchone()
            if result is None:
                return None

            password_hash, id = result

            if not bcrypt.checkpw(password.encode(), password_hash.encode()):
                return None

            return id
            # return User(id, username, first_name, middle_name, last_name)
