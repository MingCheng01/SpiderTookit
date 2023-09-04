import pymongo


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
