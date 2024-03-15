from wcferry import Wcf
from wcferry import wxmsg
from queue import Empty
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
        elif msg.sender=="gh_b05aec8ffdbd":
            if msg.content=="签到成功":
                break
        else:
            judge(msg.content)
    except Empty:
        continue  # Empty message