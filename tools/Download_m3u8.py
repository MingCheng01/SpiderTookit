import os
import re
import time
import shutil
import requests
from collections import deque
from Crypto.Cipher import AES
from .Download_byte import download_byte
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


class download_m3u8(download_byte):
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
        super(download_m3u8, self).__init__(
            Max_Thread=Max_Thread,
            Max_Rerty=Max_Rerty,
            Time_Sleep=Time_Sleep,
            Request_Timeout=Request_Timeout,
            Save_Error_Log=Save_Error_Log,
            Show_Progress_Bar=Show_Progress_Bar,
            Show_Error_Info=Show_Error_Info
        )

    def submit_task(self,
                    url: list = None,
                    headers: [dict[str, any], None] = None,
                    cookie: [dict[str, any], None] = None,
                    param: [dict[str, any], None] = None,
                    data: [dict[str, any], None] = None,
                    proxies: [dict[str, any], None] = None,
                    verify: bool = True,
                    allow_redirects: bool = True,
                    path_: str = './',
                    name: [list, None] = None,
                    type_: [list, None] = None,
                    splicing_url: str = ''
                    ):
        start_time = time.time()
        if len(url) == 0 or url == None:
            raise '当前url为空'
        if name == [] or len(name) == 0 or name == None:
            raise '当前name为空'
        if type(name) != str:
            raise 'name只支持字符串类型'
        if len(type_) == 0 or type_ == None:
            raise '当前type_为空'

        path_ = path_.replace('\\', '/')
        if path_[-1] != '/':
            path_ += '/'
        if os.path.exists(path_):
            pass
        else:
            os.makedirs(path_)
        if os.path.exists(path_ + 'ts/'):
            pass
        else:
            os.makedirs(path_ + 'ts/')
        self.path_ = path_
        self.name = name
        self.type_ = type_
        self.headers = headers
        self.cookie = cookie
        self.param = param
        self.data = data
        self.verify = verify
        self.proxies = proxies
        self.allow_redirects = allow_redirects
        m3u8_file = requests.get(url=url, headers=headers, cookies=cookie, params=param, data=data, verify=verify,
                                 proxies=proxies, allow_redirects=allow_redirects).text
        ts_list = re.findall(',\n(.*?)\n#', m3u8_file)
        self.url_queue = deque(maxlen=len(ts_list) + 1)
        len_ts = len(ts_list)
        for i in range(len_ts):
            self.url_queue.append({'url': splicing_url + ts_list[i], 'name': str(i), 'num': 0})
        self.error_list = []
        self.start()
        # 判断是否保存错误日志
        if self.Save_Error_Log:
            # 判断当前是否存在错误信息
            if self.error_list != []:
                print('存在超出最大请求次数的url,将不会对文件进行保存')
                # 删除存放ts的临时文件
                shutil.rmtree(self.path_ + 'ts/')
                self.save_log(path_=path_)
            else:
                print()
                print('当前并无错误日志')
                with open(self.path_ + self.name + '.' + self.type_, 'wb') as fp:
                    fp.write(b'')
                print('开始合并mp4')
                time.sleep(2)
                for i in range(len_ts):
                    # 读取ts数据
                    with open(self.path_ + 'ts/' + str(i) + '.ts', 'rb') as fp:
                        ts_content = fp.read()
                    # 将ts数据追加写入文件
                    with open(self.path_ + self.name + '.' + self.type_, 'ab') as fp:
                        fp.write(ts_content)
                # 删除存放ts的临时文件
                shutil.rmtree(self.path_ + 'ts/')
                if re.search('#EXT-X-KEY', m3u8_file):
                    print('视频存在加密,正在对其进行解密')
                    # 获取key_url
                    key_url = re.search('#EXT-X-KEY:(.*URI="(.*)")\n', m3u8_file)[2]
                    # 请求获取key
                    key = requests.get(url=key_url, headers=headers).content
                    # 解密视频
                    self.decode_aes(key, self.path_ + self.name + '.' + self.type_)
                    print('解密成功,文件已保存')
        print('执行结束,共耗时{}秒'.format(round(time.time() - start_time, 2)))

    def start(self):
        # 获取总任务数
        self.all_task_num = self.url_queue.__len__()
        print('当前启动为多线程m3u8下载器,线程数:{},任务数:{}'.format(self.Max_Thread, self.all_task_num))
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

    def get_(self, url_):
        # 尝试
        try:
            # 发送请求，获取响应
            respones = requests.get(url=url_['url'],
                                    headers=self.headers,
                                    cookies=self.cookie,
                                    proxies=self.proxies,
                                    verify=self.verify,
                                    params=self.param,
                                    data=self.data,
                                    allow_redirects=self.allow_redirects,
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

    def save_(self, content_, url_):
        # 保存
        with open(self.path_ + 'ts/' + str(url_['name']) + '.ts', 'wb') as f:
            f.write(content_)

    def decode_aes(self, key, fileName):
        # 读取原文件
        with open(fileName, 'rb') as fp:
            part = fp.read()
        # aes解密需要的偏移量
        iv = b'0000000000000000'
        # 解密数据
        plain_data = AES.new(key, AES.MODE_CBC, iv).decrypt(part)
        # 将解密数据写入文件
        with open(fileName, 'wb') as fp:
            fp.write(plain_data)
