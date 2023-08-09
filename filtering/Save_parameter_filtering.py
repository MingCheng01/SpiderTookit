import os

def save_to_csv_filtering(
        path_: str = '',
        file_name: str = '',
        data: list = None,
        mode: str = 'w',
        encoding: str = 'utf-8',
        errors=None,
        newline=None
):
    if file_name == '' or file_name == None or type(file_name) != str:
        raise '当前传入的file_name为空或者传入了非字符串类型的file_name'

    if os.path.exists(path_):
        pass
    else:
        os.makedirs(path_)

    if mode != 'a' and mode != 'w':
        raise '写入csv只支持"a"和"w"两种模式'
    else:
        pass

    if data == None or data == [] or type(data) != list:
        raise '当前传入的data为空或者传入了非列表类型的data'
    else:
        pass

    return True


def save_to_xlsx_filtering(
        path_: str = '',
        file_name: str = '',
        data: dict = None,
        mode: str = 'w',
        sheet_name: str = "Sheet1",
        columns: any = None,
        header: bool = True,
        index: bool = True,
):
    if file_name == '' or file_name == None or type(file_name) != str:
        raise '当前传入的file_name为空或者传入了非字符串类型的file_name'

    if os.path.exists(path_):
        pass
    else:
        os.makedirs(path_)

    if mode != 'a' and mode != 'w':
        raise '写入xlsx只支持"a"和"w"两种模式'
    else:
        pass

    if data == None or data == {} or type(data) != dict:
        raise '当前传入的data为空或者传入非字典类型的data'
    else:
        pass

    if type(header) != bool:
        raise 'header只支持传入布尔类型'
    else:
        pass

    if type(index) != bool:
        raise 'index只支持传入布尔类型'
    else:
        pass

    if mode == 'a':
        if os.path.isfile(path_ + file_name):
            pass
        else:
            raise '当前模式为追加写入,但并未发现指定文件'
    else:
        pass

    return True


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


def save_to_redis_filtering(
        host: str = 'localhost',
        port: int = 6379,
        database: str = '',
        password: str = '',
        pool_size: int = 10
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

    if pool_size == '' or type(pool_size) != int:
        raise '传入的pool_size为空或传入了非整型类型的pool_size'
    else:
        pass

    if port == '' or type(port) != int:
        raise '传入的port为空或传入了非整型类型的port'
    else:
        pass

    return True


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
