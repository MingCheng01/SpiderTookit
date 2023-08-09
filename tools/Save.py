import pandas as pd
import csv
import pymysql
import redis
import pymongo


def save_to_csv(
        path_: str = '',
        file_name: str = '',
        data: list = None,
        mode: str = 'w',
        encoding: str = 'utf-8',
        errors=None,
        newline=''
):
    with open(file=path_ + file_name, mode=mode, encoding=encoding, errors=errors, newline=newline) as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


def save_to_xlsx(
        path_: str = '',
        file_name: str = '',
        data: dict = None,
        mode: str = 'w',
        sheet_name: str = "Sheet1",
        columns: any = None,
        header: bool = True,
        index: bool = True
):
    if mode == 'w':
        df = pd.DataFrame(data)
        df.to_excel(excel_writer=path_ + file_name, index=index, sheet_name=sheet_name, columns=columns, header=header)
    if mode == 'a':
        df_old = pd.read_excel(io=path_ + file_name, sheet_name=sheet_name, index_col=0)
        df_new = pd.concat([df_old, pd.DataFrame(data)], ignore_index=True)
        df_new.to_excel(excel_writer=path_ + file_name, index=index, sheet_name=sheet_name, columns=columns,
                        header=header)


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


class save_to_redis():
    def __init__(
            self,
            host: str = 'localhost',
            port: int = 6379,
            database: str = '',
            password: str = '',
            pool_size: int = 10
    ):
        if password != '':
            self.pool = redis.ConnectionPool(host=host, port=port, db=database, password=database,
                                             max_connections=pool_size)
        else:
            self.pool = redis.ConnectionPool(host=host, port=port, db=database, max_connections=pool_size)
        self.redis_conn = redis.Redis(connection_pool=self.pool)
        self.redis_db = redis.StrictRedis(host=host, port=port, db=database)

    def put(self, key, value):
        self.redis_db.set(key, value)

    def close(self):
        self.redis_db.close()


class save_to_mongo():
    def __init__(
            self,
            host: str = 'localhost',
            port: int = 6379,
            database: str = '',
            user: str = '',
            password: str = '',
            pool_size: int = 10,
            collection: str = ''
    ):
        if user != '' and password != '':
            credentials = '{0}:{1}@'.format(user, password)
            self.client = pymongo.MongoClient('mongodb://{0}{1}:{2}/'.format(credentials, host, port),
                                              maxPoolSize=pool_size)
        else:
            self.client = pymongo.MongoClient('mongodb://{0}:{1}/'.format(host, port), maxPoolSize=pool_size)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def put(self, data):
        self.collection.insert_one(data)

    def close(self):
        self.client.close()
