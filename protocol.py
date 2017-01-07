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
