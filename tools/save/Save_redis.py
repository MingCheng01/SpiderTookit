import redis


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
