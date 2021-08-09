# -*- coding: utf-8 -*-
# @Time : 2021/8/9 10:21
# @Author :
# @Site : Beijing
# @File : tcpClient.py
# @Software: PyCharm
import json
import socket

from actionMode import action


def tcpWeb():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("8.141.75.140", 9090))

    data = {'type': 'register', 'name': 'zhuXiaoJian', 'user_name': 'zhuXiaoJian',
            'password': '666666'}
    json_str = json.dumps(data)
    json_str = bytes(json_str, encoding="utf8")

    client.send(json_str)

    data = {'type': 'login', 'user_name': 'zhuXiaoJian', 'password': '666666'}
    login_str = json.dumps(data)
    login_str = bytes(login_str, encoding="utf8")

    client.send(login_str)
    while True:
        info = client.recv(1024)
        data = json.loads(info)
        action(data['id'], data['degree'])
        print(data)


if __name__ == "__main__":
    tcpWeb()
