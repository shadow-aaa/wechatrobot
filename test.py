from wcferry import Wcf
from wcferry import wxmsg
from queue import Empty
import time
def judge(code:str):
    if code.isdigit() and len(code)==4:
        return True
    else:
        return False
def msgfromduifene():
    result=wxmsg
    while 1:
        try:
            result=robot.get_msg()
            if result.sender=="gh_b05aec8ffdbd":
                print("已接收到对分易消息")
                print(result.content)
                return result
        except Empty:
            continue
robot=Wcf(debug=True,block=True)
msg=wxmsg
result=wxmsg
print("机器人！启动！")
print("略过同步消息")
time.sleep(5)
robot.enable_receiving_msg()
print("开始接收消息")
while robot.is_receiving_msg():
    try:
        msg = robot.get_msg()
        if judge(msg.content)==True:
            robot.send_text(msg.content,"duifene")
            result=msgfromduifene()
            if result.content.find("签到成功")!=-1:
                robot.send_text(msg.content,"43806374575@chatroom")
                break
    except Empty:
        continue  # Empty message