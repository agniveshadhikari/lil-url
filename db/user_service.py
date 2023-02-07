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

    def create(self, username, password=None, first_name=None, middle_name=None, last_name=None):
        if password is None:
            password_hash = None
        else:
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        with self.connection_manager.cursor() as curs:
            curs.execute(
                """
                insert into "user" (username, password_hash, first_name, middle_name, last_name)
                values(%s, %s, %s, %s, %s)
                returning id
                """,
                (username, password_hash, first_name, middle_name, last_name))
            id, = curs.fetchone()
            return id

    def update_password(self, *args, user_id=None, username=None, password=None):
        if password is None:
            raise ValueError("Keyword argument 'password' is required")
        if (user_id is None == username is None):
            raise ValueError(
                "Exactly one of the keyword arguments ['username', 'user_id'] is required")

        password_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        with self.connection_manager.cursor() as curs:
            curs.execute(
                """
                update "user"
                set password_hash=%s
                where id=%s or username=%s
                """,
                (password_hash, user_id, username))

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
