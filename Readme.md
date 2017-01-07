# pyHttpd——socket实现的web服务器


----------
## 关于
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