from wcferry import Wcf
from wcferry import wxmsg
from queue import Empty
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
            if result.sender=="duifene":
                return result
        except Empty:
            continue
robot=Wcf(debug=True,block=True)
msg=wxmsg
result=wxmsg
robot.enable_receiving_msg()
print("开始接收信息")
while robot.is_receiving_msg():
    try:
        msg = robot.get_msg()
        if judge(msg.content)==True:
            robot.send_text(msg,"duifene")
            result=msgfromduifene()
            if result.content.find("签到失败")!=-1:
                robot.send_text(msg,"43806374575@chatroom")
                break
    except Empty:
        continue  # Empty message