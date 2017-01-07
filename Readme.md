# pyHttpd——socket实现的web服务器


----------
## 关于作品
学习计算机网络时，为了更好理解网络协议，使用socket套接字开发的简单的 web 服务器。旨在更好的理解Http工作流程和学习使用网络编程。

## 开发依赖
*pyHttpd*基于Python2 开发，使用原始socket套接字，除了多线程模块（threading），系统模块（os）等几个必需内置模块外，没有使用任何其他第三方依赖库。只要安装有Python环境，在任何平台都能稳定运行。

## 如何使用
1. 从github上克隆到本地
  `$ git clone https://github.com/Insh3ll/pyhttpd.git`
2. 进入pyhttpd目录
  `$ cd pyhttpd`
3. 执行pyhttpd.py
  `$ python pyhttd.py`  

看到如下提示说明执行成功，Http服务器处于监听状态等待连接
![启动成功][1]

## 文件解读
目录树
```shell
pyhttpd
├── config.py
├── core.py
├── protocol.py
├── pyhttpd.py
├── serverInfo.py
└── train
```
- **config.py**
> pyhttpd 启动时读取的配置文件，包括监听的IP和Port、web主目录、web默认文档、日志路径等

- **core.py**
> pyhttpd 核心文件，将*Http*协议的逻辑实现封装在**Httpd**类中，具体包括监听和响应客户端的请求等

- **protocol.py**
> pyhttpd 协议解析类，负责解析*HTTP*协议中的相关参数，被核心文件*core.py*调用

- **serverInfo.py**
> pyhttpd 响应中返回的服务器信息处理方法，包括*HTTP*状态码解析和服务信息的输出。

- ** pyhttpd.py **
> pyhttpd 的执行文件，引入*core.py*模块，生成Httpd类对象并启动

## 代码分析
- **config.py**
```python
#coding:utf-8

import random

Config = {
    'server_ip': '0.0.0.0', # 绑定的本地监听端口
    'server_port': 8090, #random.randint(8000,8100), # 8080
    'client_max': 10,   # 最大连接数
    'log_file': '/tmp/httpd.log',   # 日志文件路径

    'wwwroot': './train', # 点表示当前目录
    'default_doc': '/index.html' # 默认文档
}
```

- **core.py**
```python
# coding:utf-8

import os
import threading
import socket
import random

from protocol import Http   # Http协议解析类
from config import Config   # 配置类
from serverInfo import responseLine as rsp_line # 状态返回方法


class Httpd():

    def __init__(self):
        self.srv_ip = Config['server_ip']   # 服务器监听IP
        self.srv_port = Config['server_port']   # 服务器监听端口
        self.clt_max = Config['client_max']   # 服务器监听的最大连接数
        self.wwwroot = Config['wwwroot']    # web主目录
        self.lock = threading.Lock()

    def load(self):
        """ 启动监听 """
        self.srv = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)  # 实例化tcp类型的socket
        self.srv.bind((self.srv_ip, self.srv_port))  # 绑定端口和IP
        self.srv.listen(self.clt_max)  # 启动监听
        print("Httpd server is listening: {ip}:{port}".format(
            ip=self.srv_ip, port=self.srv_port))   # 打印服务器监听信息

    def run(self):
        """ 运行处理方法，接收客户端的请求 """
        self.load()     # 启动监听
        while True:     # 使主线程一直处于监听状态
            clt, addr = self.srv.accept()    # 接收客户端的请求，返回客户端socket对象和客户端地址
            print("Connected from {addr}".format(addr=addr))    # 打印客户端信息
            # 新开一个线程处理客户端请求
            t = threading.Thread(target=self.request_handle, args=(clt,))
            t.setDaemon(True)
            t.run()  # 启动线程处理请求

    def request_handle(self, clt):
        """ 接收数据，处理请求 """
        recv_data = ''
        recv_dataTmp = ''
        html_doc = ''
        while True:
            recv_dataTmp = clt.recv(1024)
            recv_data += recv_dataTmp
            if len(recv_dataTmp) < 1024:
                break

        try:
            ptc = Http(recv_data)   # 将接收的数据初始化Http类的对象
            self.print_info(ptc)    # 打印解析后的http参数
            if ptc.method == 'GET':     # get请求的处理方法
                self.get_handle(clt, ptc)
            elif ptc.method == 'POST':  # post请求的处理方法
                self.post_handle(clt, ptc)
            else:      # 其它请求时返回400错误
                self.error_handle(clt, 400)
        except Exception as e:
            print(e)
            self.error_handle(clt, 500)     # 请求处理失败时返回500错误，并关闭连接

        ......

```

- **protocol.py**
```python
# coding:utf-8
import re

class Http():

    """ 解析HTTP协议 """

    def __init__(self, streamData):
        self.stream = streamData
        # self.stream.split('\r\n\r\n')[0]
        self.headers = re.search(r"([\s\S]*)\r\n\r\n", self.stream).group(1)
        self.body = re.search(r"\r\n\r\n([\s\S]*)", self.stream).group(1)

    @property
    def method(self):
        return re.search(r"(GET|POST)", self.headers).group(0)

    @property
    def path(self):
        m = re.search(r"(GET|POST) (.*?) HTTP/", self.headers).group(2)
        return m.split('?')[0] if '?' in m else m

    @property
    def parameters(self):
        m = re.search(r"(GET|POST) (.*?) HTTP/", self.headers).group(2)
        return m.split('?')[1] if '?' in m else ''

    @property
    def user_agent(self):
        return re.search(r"User-Agent: (.*)", self.headers).group(1)

    @property
    def cookies(self):
        m = re.search(r"Cookie: (.*)", self.headers)
        return m.group(1) if m else ''

    @property
    def content_length(self):
        m = re.search(r"Content-Length: (.*)", self.stream)
        return m.group(1) if m else ''
```

- **serverInfo.py**
```python
# coding: utf-8
import time

srv_info = """HTTP/1.1 {statuCode}\r\nServer: z0ne_httpd/0.1\r\nDate: {date}\r\nCache-Control: no-cache\r\nContent-Language: en,zh\r\n\r\n"""

codeDict = {
    '200': '200 OK',
    '302': '302 Found',
    '400': '400 Bad Request',
    '403': '403 Forbidden',
    '404': '404 Not Found',
    '500': '500 Internal Server Error',
    '503': '503 Service Unavailable',
}


def responseLine(code):
    return srv_info.format(statuCode=codeDict.get(str(code),'400 Bad Request'),date=time.ctime())
```

## 运行时截图
![首页][2]

![查询][3]

![运行状态][4]

![日志记录][5]


  [1]: http://ww3.sinaimg.cn/large/eda5686egw1fbiauxkg3wj20bq01l74m.jpg
  [2]: http://ww4.sinaimg.cn/large/eda5686egw1fbibonfaayj211p0idq4p.jpg
  [3]: http://ww2.sinaimg.cn/large/eda5686egw1fbibp6yuvtj211q0htdh0.jpg
  [4]: http://ww1.sinaimg.cn/large/eda5686egw1fbibuha2jej211r0gjqdh.jpg
  [5]: http://ww2.sinaimg.cn/large/eda5686egw1fbibwu074jj210u0g2wn4.jpg