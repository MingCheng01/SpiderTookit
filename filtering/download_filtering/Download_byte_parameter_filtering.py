import os


def donwload_byte_filtering(
        Max_Thread: int = 0,
        Max_Rerty: int = 3,
        Time_Sleep: [float, int] = 0,
        Request_Timeout: [float, int] = 10,
        Save_Error_Log: bool = True,
        Show_Progress_Bar: bool = False,
        Show_Error_Info: bool = True
):

    if type(Max_Thread) != int:
        raise '设置的MAX_THREAD不为整型'
    else:
        pass

    if type(Max_Rerty) != int:
        raise '设置的MAX_RETRY不为整型'
    else:
        pass

    if type(Time_Sleep) != float or type(Time_Sleep) != int or type(Time_Sleep) != list:
        pass
    else:
        raise '设置的Time_Sleep不为整型,浮点型或列表'

    if type(Request_Timeout) != float or type(Request_Timeout) != int:
        pass
    else:
        raise '设置的的Request_Timeout不为整型或浮点型'

    if Save_Error_Log != True and Save_Error_Log != False:
        raise '错误日志保存设置只支持传入布尔类型'
    else:
        pass

    if Show_Progress_Bar != True and Show_Progress_Bar != False:
        raise '进度条设置只支持传入布尔类型'
    else:
        pass

    if Show_Error_Info != True and Show_Error_Info != False:
        raise '错误信息显示设置只支持传入布尔类型'
    else:
        pass

    return True


def donwload_byte_function_filtering(
        url: str = None,
        headers: [dict[str, any], None] = None,
        cookie: [dict[str, any], None] = None,
        param: [dict[str, any], None] = None,
        data: [dict[str, any], None] = None,
        proxies: [dict[str, any], None] = None,
        verify: bool = True,
        path_: str = './',
        name: str = '',
        type_: str = ''
):
    if len(url) < 1 or url == None:
        raise '未传入url或url为空'
    else:
        pass

    if type(name) != str:
        raise 'name只支持传入字符串类型'

    if type(type_) != str:
        raise 'type_只支持传入字符串类型'

    if os.path.exists(path_):
        pass
    else:
        os.makedirs(path_)

    return True
