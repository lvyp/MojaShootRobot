# -*- coding: utf-8 -*-
# @Time : 2021/8/9 10:21
# @Author :
# @Site : Beijing
# @File : tcpClient.py
# @Software: PyCharm
import ast
import json
import socket
import time

from canMotor import CanMotor
from comMotor import ComMotor

TIMEOUT = 0.1

def tcpWeb():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("8.141.75.140", 9090))

    data = {'type': 'register', 'name': 'zhuXiaoJian', 'user_name': 'zhuXiaoJian',
            'password': '666666'}
    json_str = json.dumps(data)
    json_str = bytes(json_str, encoding="utf8")

    client.send(json_str)
    info = client.recv(1024)
    data = json.loads(info)

    data = {'type': 'login', 'user_name': 'zhuXiaoJian', 'password': '666666'}
    login_str = json.dumps(data)
    login_str = bytes(login_str, encoding="utf8")

    client.send(login_str)
    info = client.recv(1024)
    data = json.loads(info)

    comMotor = ComMotor("COM1")
    canMotor = CanMotor()
    canMotor.RUN_CAN()
    canMotor.MOTOR_INIT(16)
    canMotor.MOTOR_INIT(17)
    canMotor.MOTOR_INIT(18)
    while True:
        infoBytes = client.recv(1024)
        infoStr = str(infoBytes, encoding="utf-8")
        infoList = ast.literal_eval(infoStr)
        for info in infoList:
            if info['degree'] != "":
                if info['id'] < 16:
                    time.sleep(TIMEOUT)
                    comMotor.action(info['id'], info['degree'])
                else:
                    time.sleep(TIMEOUT)
                    canMotor.MOTOR_Ctr(info['id'], info['degree'])
                print(info)
            else:
                pass


if __name__ == "__main__":
    tcpWeb()
