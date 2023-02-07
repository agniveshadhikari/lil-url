from .connection_manager import AbstractConnectionManager

class RedirectService:
    def __init__(self, connection_manager: AbstractConnectionManager) -> None:
        self.connection_manager = connection_manager

    def create(self, path, target, user_id, expire_time=None):
        with self.connection_manager.cursor() as curs:
            curs.execute(
                """
                select id
                from redirect
                where path=%s
                    and expire_time > CURRENT_TIMESTAMP
                    and delete_time is NULL
                """,
                (path,)
            )
            if curs.rowcount > 1:
                # TODO: Log error
                pass
            if curs == 1:
                raise Exception("Link already exists.")
            curs.execute(
                """
                insert into redirect (path, target, owner, expire_time)
                values(%s, %s, %s, %s)
                """,
                (path, target, user_id, expire_time))

    def get_active_target(self, path) -> str:
        with self.connection_manager.cursor() as curs:
            curs.execute(
                """
                select target
                from redirect
                where path=%s
                    and activate_time <= CURRENT_TIMESTAMP
                    and (expire_time >= CURRENT_TIMESTAMP or expire_time is NULL)
                    and delete_time is NULL
                order by create_time desc
                """,
                (path,))
            if curs.rowcount > 1:
                # TODO: Log error
                pass
            result = curs.fetchone()
            if result != None:
                return result[0]
            return None

    def get_all(self, user_id):
        with self.connection_manager.cursor() as curs:
            curs.execute(
                """
                select path, target
                from redirect
                where owner=%s
                    and activate_time <= CURRENT_TIMESTAMP
                    and (expire_time >= CURRENT_TIMESTAMP or expire_time is NULL)
                    and delete_time is NULL
                order by create_time desc
                """,
                (user_id,))
            result = curs.fetchall()
            if result != None:
                return result
            return None

    def delete(self, path):
        with self.connection_manager.cursor() as curs:
            curs.execute(
                """
                delete from redirect
                where path=%s
                """,
                (path,)
            )
