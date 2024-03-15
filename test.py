from wcferry import Wcf
from wcferry import wxmsg
from queue import Empty
def judge(newcode:str):
    global oldcode
    if newcode.isdigit() and len(newcode)==4:
        if oldcode=="":#第一次接收到签到码
            oldcode=newcode
            print("接收到签到码，正在发送")
            robot.send_text(newcode,"43806374575@chatroom")
            robot.send_text(newcode,"duifene")
        elif oldcode==newcode:#群里的人再次发送签到码，且签到码是假的，导致没有退出机器人
            print("与前一个签到码一致")
            print("不进行签到")
            pass
        else:#新码
            print("接收到签到码，正在发送")
            robot.send_text(newcode,"43806374575@chatroom")
            robot.send_text(newcode,"duifene")
    else:
        print("等待签到码中")

robot=Wcf(debug=False,block=True)
msg=wxmsg
oldcode=""
robot.enable_receiving_msg()
print("开始接收信息")
while robot.is_receiving_msg():
    try:
        msg = robot.get_msg()
        if msg.from_self():
            pass
        elif msg.sender=="gh_b05aec8ffdbd":
            if msg.content.find("签到成功"):
                break
        else:
            judge(msg.content)
    except Empty:
        continue  # Empty message