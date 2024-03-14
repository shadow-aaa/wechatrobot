from wcferry import Wcf
from wcferry import wxmsg
from queue import Empty
import time
def judge(str1:str):
    if str1.isdigit() and len(str1)==4:
        print("接收到签到码，正在发送")
        robot.send_text(str1,"43806374575@chatroom")
        robot.send_text(str1,"duifene")
        return True
    else:
        print("等待签到码中")
        return False
robot=Wcf(debug=False,block=True)
msg=wxmsg
robot.enable_receiving_msg()
print("开始接收信息")
while robot.is_receiving_msg():
    try:
        msg = robot.get_msg()
        if msg.from_self():
            pass
        else:
            sendcode=judge(msg.content)
            if sendcode:
                time.sleep(1.5)
                msg=robot.get_msg() #接收对分易反馈
                print(msg.content)
    except Empty:
        continue  # Empty message