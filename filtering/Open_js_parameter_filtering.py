import os
def open_js_filtering(
        path_: str = '',
        encoding: str = 'utf-8',
        cwd: any = None
):
    if os.path.isfile(path_):
        pass
    else:
        raise '未找到该文件'
    return True
