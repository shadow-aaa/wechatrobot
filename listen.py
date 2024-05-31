from mitmproxy import http, ctx
import os
from subprocess import Popen
url = "https://www.duifene.com/app_ck/b.ashx"

latest_lc = None
lc_file_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'lc.txt')

def response(flow: http.HTTPFlow):
    global latest_lc
    text = flow.response.get_text()
    if "所在班级当前没有正在进行的签到" in text:
        # ctx.log.info("登录代码的值为")
        # ctx.log.info(latest_lc)
        with open(lc_file_path,'w') as f:
            f.write(latest_lc)
        # ctx.log.info("已写入登录代码至文件")
        close_listen()

def request(flow: http.HTTPFlow) -> None:
    global latest_lc
    if flow.request.pretty_url == url and flow.request.method == "POST":
        data = flow.request.content.decode('utf-8')
        lc_value = data.split("lc=")[1].split("&")[0]
        latest_lc = lc_value
        # ctx.log.info("找到登录代码了！！！！！！！！！！！！！！！！！！")

def close_listen():
    Popen('winproxy off', stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w')).communicate()
    result = os.popen('netstat -ano | findstr 7654 | findstr LISTENING')
    port = result.read().split('      ')[-1]
    if port:
        Popen(f'taskkill /f -t /pid {port}', stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))