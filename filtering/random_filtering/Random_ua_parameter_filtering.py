def random_ua_filtering(
        factory: str = 'random'
):
    if factory != 'random' or factory != 'chrome' or factory != 'firefox' or factory != 'ie':
        pass
    else:
        raise '目前ua生成不支持该内核'
    return True
