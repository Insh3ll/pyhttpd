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

    def get_handle(self, clt, ptc):
        """ 处理GET请求 """
        file_path = self.path_match(ptc.path)
        if os.path.isfile(file_path):   # 请求的资源文件存在时
            with open(file_path) as f:  # 读取请求的资源文件
                html_doc = f.read()
                # 拼接返回数据
            rsp_data = rsp_line(200).replace('\r\n\r\n','\r\nContent-Length: %s\r\n\r\n%s' % (len(html_doc),html_doc),1)
            clt.send(rsp_data)   # 将资源文件发给客户端
            clt.close()     # 关闭连接
        else:
            self.error_handle(clt, 404)

    def post_handle(self, clt, ptc):
        """ 处理POST请求 """
        self.get_handle(clt,ptc)

    def error_handle(self, clt, code):
        """ 处理错误请求 """
        clt.send(rsp_line(code))    # 请求资源不存在时返回404，并关闭连接
        clt.close()
        return 0
        

    def path_match(self, path):
        """ 请求路径和本地资源路径的匹配 """
        if path == '/':
            return self.wwwroot + Config['default_doc']
        return self.wwwroot + path

    def print_info(self, ptc):
        """ 打印相关的信息 """
        self.lock.acquire()
        print("{headers}\n".format(headers=ptc.headers))
        with open(Config['log_file'],'a+') as f:
            f.write(ptc.headers)
        self.lock.release()


if __name__ == '__main__':
    srv = Httpd()
    srv.run()
