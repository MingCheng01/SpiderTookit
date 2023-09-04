import execjs
import os

def open_js(
        path_: str = '',
        encoding: str = 'utf-8',
        cwd: any = None
):
    if os.path.exists(path_):
        with open(path_, 'r', encoding=encoding) as f:
            return execjs.compile(f.read(), cwd)
    else:
        raise '文件不存在'
