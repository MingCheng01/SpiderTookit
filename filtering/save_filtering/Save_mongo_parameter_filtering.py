def save_to_mongo_filtering(
        host: str = 'localhost',
        port: int = 6379,
        database: str = '',
        user: str = '',
        password: str = '',
        pool_size: int = 10,
        collection: str = ''
):
    if database == '' or type(database) != str:
        raise '传入的database为空或传入了非字符串类型的database'
    else:
        pass

    if password == '' or type(password) != str:
        raise '传入的password为空或传入了非字符串类型的password'
    else:
        pass

    if user == '' or type(user) != str:
        raise '传入的user为空或传入了非字符串类型的user'
    else:
        pass

    if host == '' or type(host) != str:
        raise '传入的host为空或传入了非字符串类型的host'
    else:
        pass

    if collection == '' or type(collection) != str:
        raise '传入的collection为空或传入了非字符串类型的collection'
    else:
        pass

    if pool_size == '' or type(pool_size) != int:
        raise '传入的pool_size为空或传入了非整型类型的pool_size'
    else:
        pass

    if port == '' or type(port) != int:
        raise '传入的port为空或传入了非整型类型的port'
    else:
        pass

    return True
