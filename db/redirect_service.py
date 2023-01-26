class RedirectService:
    def __init__(self, get_connection, put_connection) -> None:
        self.get_connection = get_connection
        self.put_connection = put_connection

    def create(self, path, target, user_id, expire_time=None):
        conn = self.get_connection()
        with conn.cursor() as curs:
            curs.execute("insert into redirect (path, target, user_id, expire_time) values(%s, %s, %s, %s)",
                         (path, target, user_id, expire_time))
