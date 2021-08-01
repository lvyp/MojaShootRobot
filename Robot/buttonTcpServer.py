# -*- coding: utf-8 -*-
# @Time : 2021/8/1 11:16
# @Author :
# @Site : Beijing
# @File : buttonTcpServer.py
# @Software: PyCharm
import threading
import datetime
import globalVariable
from socket import *


def minChangeToSec(h, m, s):
    s = h * 60 * 60 + m * 60 + s
    return s


def timerMachine(startTime=0.000):
    dt_hms = datetime.datetime.now().strftime('%H:%M:%S.%f')
    h, m, s = dt_hms.strip().split(":")
    hms = minChangeToSec(float(h), float(m), float(s))
    # print("m: " + m + " s: " + s + " ms: " + str(ms) + " startTime: " + str(startTime))
    return float('%.3f' % (hms - startTime))


class TcpServer(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.pushButton = 0  # 按压按钮，关闭：偶数；开启：单数
        self.server_ip = "192.168.1.49"
        self.server_port = 9527
        self.tcp_server_socket = None
        self.client_socket = None
        self.initTime = 0.000
        self.createSocket()

    def __new__(cls, *args, **kwargs):
        if not hasattr(TcpServer, "_instance"):
            with TcpServer._instance_lock:
                if not hasattr(TcpServer, "_instance"):
                    TcpServer._instance = object.__new__(cls)
        return TcpServer._instance

    def createSocket(self):
        # 创建socket
        self.tcp_server_socket = socket(AF_INET, SOCK_STREAM)
        # 本地信息
        address = (self.server_ip, self.server_port)
        # 绑定
        self.tcp_server_socket.bind(address)
        # 使用socket创建的套接字默认的属性是主动的，使用listen将其变为被动的，这样就可以接收别人的链接了
        self.tcp_server_socket.listen(128)
        # 如果有新的客户端来链接服务器，那么就产生一个新的套接字专门为这个客户端服务
        # client_socket用来为这个客户端服务
        # tcp_server_socket就可以省下来专门等待其他新客户端的链接
        self.client_socket, clientAddr = self.tcp_server_socket.accept()

    def recvMessage(self):
        # 接收对方发送过来的数据
        recv_data = self.client_socket.recv(10)  # 接收10个字节

        currentTime = timerMachine()

        if len(recv_data.decode('utf-8')) > 0:
            print(recv_data.decode('utf-8') + "\r\n")
            self.client_socket.send("successful".encode('utf-8'))

            if self.initTime == 0:
                self.pushButton += 1
                self.initTime = currentTime

            # 30为游戏时长，单位秒
            if (currentTime - self.initTime) > 30:
                self.pushButton += 1
            elif currentTime - self.initTime == 0:
                print("初次按钮触发")
            else:
                print("该时间段按钮触发无效")

            if self.pushButton % 2 == 0:
                self.pushButton = 0
                self.initTime = 0
                # 设置初始点运动位置
                globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_init_target_list())
                globalVariable.set_value("mapRouteSettingInitPointFlag", True)
                globalVariable.set_value("scoreFlag", False)
                print("关闭")
            else:
                if currentTime - self.initTime == 0:
                    globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_target_list())
                    globalVariable.set_value("mapRouteSettingFlag", True)
                    globalVariable.set_value("scoreFlag", True)
                    print("开启")
            # print(self.pushButton)
        else:
            pass

    def closeSocket(self):
        self.client_socket.close()
        self.tcp_server_socket.close()
