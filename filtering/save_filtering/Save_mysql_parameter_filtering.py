def save_to_mysql_filtering(
        host: str = 'localhost',
        port: int = 3306,
        user: str = 'root',
        password: str = '',
        database: str = '',
        charset: str = 'utf8'
):
    if database == '' or type(database) != str:
        raise '传入的database为空或传入了非字符串类型的database'
    else:
        pass

    if password == '' or type(password) != str:
        raise '传入的password为空或传入了非字符串类型的password'
    else:
        pass

    if host == '' or type(host) != str:
        raise '传入的host为空或传入了非字符串类型的host'
    else:
        pass

    if user == '' or type(user) != str:
        raise '传入的user为空或传入了非字符串类型的user'
    else:
        pass

    if port == '' or type(port) != int:
        raise '传入的port为空或传入了非整型类型的port'
    else:
        pass

    return True
