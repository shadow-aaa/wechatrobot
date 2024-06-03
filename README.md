# wechatrobot

以独立签到为目的，基于[wechatferry](https://github.com/lich0821/WeChatFerry)实现的对分易签到机器人

在获得微信消息时可以自动签到

原理：基于mitmproxy获取lc字段登录代码，使用request发包进行签到，而无需打开快速签到小程序

[必须保持这个版本的微信](https://github.com/lich0821/WeChatFerry/releases/latest)

## 使用方法

1. 下载本项目所有文件到一个文件夹
2. 使用`pip install -r requirements.txt`来安装本项目需要的库
3. 安装且仅需要安装mitmproxy的CA证书，而不是mitmproxy，安装方法可参考：https://blog.csdn.net/feiyu68/article/details/119665869
4. 运行main.py文件（注意终端的使用提示）

## 已知bug

存放的路径有空格的话无法进行监听

## 如果喜欢不妨点个star
