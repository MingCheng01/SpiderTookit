import sys
import os
import time
import requests
import datetime
from collections import deque
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


class download_byte():
    # 初始化部分参数
    def __init__(
            self,
            Max_Thread: int = 0,
            Max_Rerty: int = 3,
            Time_Sleep: [float, int] = 0,
            Request_Timeout: [float, int] = 10,
            Save_Error_Log: bool = True,
            Show_Progress_Bar: bool = False,
            Show_Error_Info: bool = True
    ):
        self.Max_Thread = Max_Thread
        self.Max_Rerty = Max_Rerty
        self.Time_Sleep = Time_Sleep
        self.Request_Timeout = Request_Timeout
        self.Save_Error_Log = Save_Error_Log
        self.Show_Progress_Bar = Show_Progress_Bar
        self.Show_Error_Info = Show_Error_Info

    def submit_task(self,
                    urls: list = None,
                    headers: [dict[str, any], None] = None,
                    cookie: [dict[str, any], None] = None,
                    param: [dict[str, any], None] = None,
                    data: [dict[str, any], None] = None,
                    proxies: [dict[str, any], None] = None,
                    verify: bool = True,
                    allow_redirects: bool = True,
                    path_: str = './',
                    name: [list, None] = None,
                    type_: [list, None] = None
                    ):
        start_time = time.time()
        self.urls_len = len(urls)
        if urls == [] or self.urls_len == 0 or urls == None:
            raise '当前urls为空'
        if name == [] or len(name) == 0 or name == None:
            raise '当前name为空'
        if type(name) != list:
            raise 'name只支持列表类型'
        if len(name) != self.urls_len:
            raise 'name长度与urls不匹配'
        if type_ == [] or len(type_) == 0 or type_ == None:
            raise '当前type_为空'
        if type(type_) == list and len(name) != self.urls_len:
            raise 'type_长度与urls不匹配'
        if type(type_) == str:
            type_ = [type_ for i in range(self.urls_len)]

        if headers == list:
            headers_list = self.distribution_param(headers)
        else:
            headers_list = [headers for i in range(self.urls_len)]
        if cookie == list:
            cookie_list = self.distribution_param(cookie)
        else:
            cookie_list = [cookie for i in range(self.urls_len)]
        if param == list:
            param_list = self.distribution_param(param)
        else:
            param_list = [param for i in range(self.urls_len)]
        if data == list:
            data_list = self.distribution_param(data)
        else:
            data_list = [data for i in range(self.urls_len)]
        if proxies == list:
            proxies_list = self.distribution_param(proxies)
        else:
            proxies_list = [proxies for i in range(self.urls_len)]
        path_ = path_.replace('\\', '/')
        if path_[-1] != '/':
            path_ += '/'
        if os.path.exists(path_):
            pass
        else:
            os.makedirs(path_)
        # 创建双相对列
        self.url_queue = deque(maxlen=len(urls) + 1)
        # 创建错误日志列表
        self.error_list = []
        # 将url写入对列
        for i in range(len(urls)):
            u = {'url': urls[i], 'header': headers_list[i], 'cookie': cookie_list[i], 'param': param_list[i],
                 'data': data_list[i], 'proxies': proxies_list[i], 'verify': verify, 'allow_redirects': allow_redirects,
                 'num': 0, 'path': path_,
                 'name': name[i], 'type': type_[i]}
            self.url_queue.append(u)
        self.start()
        # 判断是否保存错误日志
        if self.Save_Error_Log:
            # 判断当前是否存在错误信息
            if self.error_list != []:
                self.save_log(path_=path_)
            else:
                print()
                print('当前并无错误日志')
        print('执行结束,共耗时{}秒'.format(round(time.time() - start_time, 2)))

    def start(self):
        # 获取总任务数
        self.all_task_num = self.url_queue.__len__()
        print('当前启动为单线程下载器,任务数:{}'.format(self.all_task_num))

        # 判断是否开启进度条
        if self.Show_Progress_Bar:
            # 循环执行
            while bool(self.url_queue):
                # 取出交给请求函数
                self.get_(url_=self.url_queue.popleft())
                # 打印进度条
                self.progress_bar(self.all_task_num - self.url_queue.__len__(), self.all_task_num)
        else:
            # 循环执行
            while bool(self.url_queue):
                # 取出交给请求函数
                self.get_(url_=self.url_queue.popleft())

    def get_(self, url_):
        # 尝试
        try:
            # 发送请求，获取响应
            respones = requests.get(url=url_['url'],
                                    headers=url_['header'],
                                    cookies=url_['cookie'],
                                    proxies=url_['proxies'],
                                    verify=url_['verify'],
                                    params=url_['param'],
                                    data=url_['data'],
                                    allow_redirects=url_['allow_redirects'],
                                    timeout=self.Request_Timeout)
            # 判断响应码
            if respones.status_code == 200:
                # 提交给保存函数
                self.save_(respones.content, url_)
            else:
                # 打印错误,执行except分支
                raise Exception('响应码:{}，请求失败'.format(respones.status_code))
        except Exception as e:
            # 交由判断函数，判断
            self.error_prompt(e, url_)
        # 休眠
        time.sleep(self.Time_Sleep)

    def distribution_param(self, param_):
        param_lens = len(param_)
        param_len = self.urls_len / param_lens
        if param_len % 1 > 0:
            param_len = int(param_len) + 1
        else:
            param_len = int(param_len)
        lens = param_len
        param__ = []
        for i in range(self.urls_len):
            if lens != 0:
                lens -= 1
                param__.append(param_[-param_lens])
            else:
                lens = param_len
                lens -= 1
                param_lens -= 1
                param__.append(param_[-param_lens])
        return param__

    def error_prompt(self, e, url_):
        # 判断是否超出最大次数
        if url_['num'] < self.Max_Rerty:
            # 判断是否打印信息
            if self.Show_Error_Info:
                print('当前url：{}\n出现异常：{}\n未超出指定重试次数({}/{})，将添加回对列\n'.format(url_['url'],
                                                                            e,
                                                                            url_['num'] + 1,
                                                                            self.Max_Rerty))
            # 重试次数+1
            url_['num'] = url_['num'] + 1
            # 添加回对列
            self.url_queue.append(url_)
        else:
            # 判断是否打印信息
            if self.Show_Error_Info:
                print('当前url：{}\n出现异常：{}\n超出指定重试次数({})，将写入错误列表\n'.format(url_['url'],
                                                                         e,
                                                                         self.Max_Rerty))
            # 添加回错误列表
            self.error_list.append({'url': url_['url'], 'num': url_['num'] + 1, 'log': e})

    def save_(self, content_, url_):
        # 保存
        with open(url_['path'] + str(url_['name']) + '.' + url_['type'], 'wb') as f:
            f.write(content_)

    def progress_bar(self, finish_tasks_number, all_task_number):
        # 进度条打印
        percentage = round(finish_tasks_number / all_task_number * 100)
        print("\r下载进度: {}% -> ".format(percentage), "▓" * (percentage // 2),
              '({}/{})'.format(finish_tasks_number, all_task_number), end="")
        sys.stdout.flush()

    def save_log(self, path_):
        # 保存错误日志
        with open(path_ + datetime.datetime.now().strftime("%Y年%m月%d日_%H时%M分%S秒") + '_log.txt', 'w',
                  encoding='utf-8') as f:
            for i in self.error_list:
                f.write(str(i) + '\n')


class thread_download_byte(download_byte):
    # 初始化部分参数
    def __init__(
            self,
            Max_Thread: int = 0,
            Max_Rerty: int = 3,
            Time_Sleep: [float, int] = 0,
            Request_Timeout: [float, int] = 10,
            Save_Error_Log: bool = True,
            Show_Progress_Bar: bool = False,
            Show_Error_Info: bool = True
    ):
        super(thread_download_byte, self).__init__(
            Max_Thread=Max_Thread,
            Max_Rerty=Max_Rerty,
            Time_Sleep=Time_Sleep,
            Request_Timeout=Request_Timeout,
            Save_Error_Log=Save_Error_Log,
            Show_Progress_Bar=Show_Progress_Bar,
            Show_Error_Info=Show_Error_Info
        )

    def start(self):
        # 获取总任务数
        self.all_task_num = self.url_queue.__len__()
        print('当前启动为多线程下载器,线程数:{},任务数:{}'.format(self.Max_Thread, self.all_task_num))
        # 创建线程池
        self.threadpool = ThreadPoolExecutor(max_workers=self.Max_Thread)

        # 判断是否开启进度条
        if self.Show_Progress_Bar:
            # 循环
            while bool(self.url_queue):
                # 判断队列内长度是否大于等于最大线程数
                if self.url_queue.__len__() >= self.Max_Thread:
                    # 循环提交线程写入任务列表
                    self.all_task = [self.threadpool.submit(self.get_, self.url_queue.popleft()) for i in
                                     range(self.Max_Thread)]
                    # 等待任务执行结束
                    wait(self.all_task, return_when=ALL_COMPLETED, timeout=self.Request_Timeout)
                else:
                    # 循环提交线程写入任务列表
                    self.all_task = [self.threadpool.submit(self.get_, self.url_queue.popleft()) for i in
                                     range(self.url_queue.__len__())]
                    # 等待任务执行结束
                    wait(self.all_task, return_when=ALL_COMPLETED, timeout=self.Request_Timeout)
                # 打印进度
                self.progress_bar(self.all_task_num - self.url_queue.__len__(), self.all_task_num)
        else:
            # 循环
            while bool(self.url_queue):
                # 判断队列内长度是否大于等于最大线程数
                if self.url_queue.__len__() >= self.Max_Thread:
                    # 循环提交线程写入任务列表
                    self.all_task = [self.threadpool.submit(self.get_, self.url_queue.popleft()) for i in
                                     range(self.Max_Thread)]
                    # 等待任务执行结束
                    wait(self.all_task, return_when=ALL_COMPLETED, timeout=self.Request_Timeout)
                else:
                    # 循环提交线程写入任务列表
                    self.all_task = [self.threadpool.submit(self.get_, self.url_queue.popleft()) for i in
                                     range(self.url_queue.__len__())]
                    # 等待任务执行结束
                    wait(self.all_task, return_when=ALL_COMPLETED, timeout=self.Request_Timeout)


def donwload_byte_function(
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
    respones = requests.get(url=url, headers=headers, cookies=cookie, proxies=proxies,
                            verify=verify, params=param, data=data)
    if respones.status_code == 200:
        with open(path_ + name + '.' + type_, 'wb') as f:
            f.write(respones.content)
    else:
        raise Exception('响应码:{}，请求失败'.format(respones.status_code))
