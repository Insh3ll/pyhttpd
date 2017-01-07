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
