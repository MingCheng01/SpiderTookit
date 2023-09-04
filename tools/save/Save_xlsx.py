import pandas as pd
import os


def save_to_xlsx(
        path_: str = '',
        file_name: str = '',
        data: dict = None,
        mode: str = 'w',
        sheet_name: str = "Sheet1",
        columns: any = None,
        header: bool = True,
        index: bool = True
):
    if mode == 'w':
        df = pd.DataFrame(data)
        df.to_excel(excel_writer=path_ + file_name, index=index, sheet_name=sheet_name, columns=columns, header=header)
    if mode == 'a':
        if os.path.exists(path_ + file_name):
            df_old = pd.read_excel(io=path_ + file_name, sheet_name=sheet_name, index_col=0)
        else:
            df_old = pd.DataFrame()
        df_new = pd.concat([df_old, pd.DataFrame(data)], ignore_index=True)
        df_new.to_excel(excel_writer=path_ + file_name, index=index, sheet_name=sheet_name, columns=columns,
                        header=header)
