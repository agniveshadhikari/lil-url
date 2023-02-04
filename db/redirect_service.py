from .connection_manager import AbstractConnectionManager

class RedirectService:
    def __init__(self, connection_manager: AbstractConnectionManager) -> None:
        self.connection_manager = connection_manager

    def create(self, path, target, user_id, expire_time=None):
        conn = self.connection_manager.get_connection()
        with conn.cursor() as curs:
            curs.execute(
                """
                select id
                from redirect
                where path=%s
                    and expire_time > CURRENT_TIMESTAMP
                    and delete_time == NULL
                """
            )
            if curs.rowcount > 1:
                # TODO: Log error
                pass
            if curs == 1:
                raise Exception("Link already exists.")
            curs.execute(
                """
                insert into redirect (path, target, user_id, expire_time)
                values(%s, %s, %s, %s)
                """,
                (path, target, user_id, expire_time))

    def get_active_target(self, path) -> str:
        conn = self.connection_manager.get_connection()
        with conn.cursor() as curs:
            curs.execute(
                """
                select target
                from redirect
                where path=%s
                    and activate_time <= CURRENT_TIMESTAMP
                    and expire_time >= CURRENT_TIMESTAMP
                    and delete_time is NULL
                order by create_time desc
                """,
                (path,))
            print("Executed SQL:", curs.query)
            if curs.rowcount > 1:
                # TODO: Log error
                pass
            result = curs.fetchone()
            if result != None:
                return result[0]
            return None
