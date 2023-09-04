import pymysql


class save_to_mysql():
    def __init__(
            self,
            host: str = 'localhost',
            port: int = 3306,
            user: str = 'root',
            password: str = '',
            database: str = '',
            charset: str = 'utf8'
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=self.charset
        )

    def insert(self, table, data):
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"insert into {table} ({keys}) values ({values})"
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, list(data.values()))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False

    def close(self):
        self.conn.close()
