import csv


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
