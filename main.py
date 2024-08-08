from wcferry import Wcf
import requests
import json
import urllib.parse
import urllib3
from mitmproxy.tools.main import mitmdump
from queue import Empty
import os
import time
from subprocess import Popen
# 数据包部分开始
url = "https://www.duifene.com/app_ck/b.ashx"
headers = {
    "Xweb_xhr": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090217) XWEB/9129",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://servicewechat.com/wx403e50de78507957/2/page-frame.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}
# 固定的postdata
fixed_postdata = {
    "a": "checkin",
    "lc": ""
}
data_field = {
    "action": "ck_df",
    "code": "",
    "typeid": 1,
    "accesstype": 6
}
# 只有lc和code需要获取，code为签到码，通过微信聊天获取
# 数据包部分结束


def codejudge(code: str):  # 接收并判断消息是否为四位数字
    return code.isdigit() and len(code) == 4


def checkin(code: str):  # 发起签到
    data_field["code"] = code
    encoded_data_field = urllib.parse.quote(
        json.dumps(data_field, separators=(',', ':')))
    finaldata = f"a={fixed_postdata['a']}&lc={fixed_postdata['lc']}&data={encoded_data_field}"
    response = requests.post(url, headers=headers,
                             data=finaldata, verify=False)
    print(response.content.decode('utf-8'))  # 用于显示签到结果
    if "签到成功" in response.content.decode("utf-8"):
        # 签到成功后通过群聊id转发给指定的群聊，群聊id可以通过机器人的其它函数获取
        robot.send_text(code, "43806374575@chatroom")
        robot.send_text("大的来了，都别睡", "43806374575@chatroom")


def start_listen():  # 开启另一个进程，监听lc
    script_path = os.path.dirname(os.path.abspath(__file__))
    Popen('winproxy set --all 127.0.0.1:7654', stdout=open(os.devnull,
          'w'), stderr=open(os.devnull, 'w')).communicate()
    time.sleep(0.2)
    Popen('winproxy on', stdout=open(os.devnull, 'w'),
          stderr=open(os.devnull, 'w')).communicate()
    time.sleep(0.2)
    print("系统代理端口已更改至7654")
    print("开始监听")
    Popen(f'mitmdump -s {script_path}/listen.py -p 7654',
          stdout=open(os.devnull, 'w'))
#   对终端信息进行了删除


def getlc():  # 拼接监听到的lc
    while True:
        try:
            with open(lc_file_path, 'r') as f:
                fixed_postdata['lc'] = f.read().strip()
                break
        except FileNotFoundError:
            print("请手动打开对分易的快速签到，随便输入签到码进行签到，程序会监听登录代码")
            time.sleep(2)


def clearlc():  # 清楚残余文本文件
    if (os.path.isfile(lc_file_path)):
        os.remove(lc_file_path)


# 定义lc路径
lc_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'lc.txt')

urllib3.disable_warnings()

# 定义机器人
robot = Wcf(debug=False, block=True)

if __name__ == "__main__":
    # 机器人启动显示
    print("机器人！启动！")
    print("略过同步消息")
    time.sleep(5)
    # 对分易同时接收太多签到码会禁止账号签到
    robot.enable_receiving_msg()
    # 清除上一次的lc代码后开始监听本次lc代码，获得lc后清除通信用文本文件
    clearlc()
    start_listen()
    getlc()
    clearlc()

    print("监听已结束，系统代理已关闭，请注意与其它代理软件的冲突")
    print("登录代码已获取，等待签到码中")

    while robot.is_receiving_msg():
        try:
            msg = robot.get_msg()
            if codejudge(msg.content):
                checkin(msg.content)
        except Empty:
            continue
