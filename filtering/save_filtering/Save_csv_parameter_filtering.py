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
