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
