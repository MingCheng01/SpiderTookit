import os


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
