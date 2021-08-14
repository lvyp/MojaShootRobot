# -*- coding: utf-8 -*-
# @Time : 2021/6/29 16:21
# @Author :
# @Site : Beijing
# @File : serialClass.py
# @Software: PyCharm
import json
import threading
import binascii
import serial
import globalVariable
import serial.tools.list_ports
from loggerMode import logger


def parityBit(Data):
    bytesData = bytes(Data, encoding="ascii")
    HexData = binascii.b2a_hex(bytesData)
    hexStrNumber = len(HexData)
    HexData = HexData.decode("utf-8")
    parity = int(hex(int(hexStrNumber/2)), 16)
    step = 2
    for i in range(int(hexStrNumber/2)):
        parity = parity ^ int(HexData[i*2:i*2+step], 16)
    return parity


class Serial(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.serialFd = 0
        self.targetList = {}
        self.initTargetList = {}
        self.availableDataList = []
        self.getAvailableSerialList()
        self.powerOn()
        self.recvMessage()
        self.connectWifi()
        self.recvMessage()
        self.wifiIp()
        self.recvMessage()
        with open("targetList.txt", "r", encoding='UTF-8') as f:
            self.target = json.load(f)
            print(self.target)
        with open("initPosition.txt", "r", encoding='UTF-8') as f:
            self.initTarget = json.load(f)
            print(self.initTarget)
        self.set_target_List()
        self.set_init_target_List()

    # 设置运动目标点列表
    def set_target_List(self):
        head = "nav:set_flag_point"
        tail = "]"
        for key in self.target:
            message = ""
            for i in range(len(self.target[key])):
                self.target[key][i] = str(self.target[key][i])
                if i == 0:
                    symbol = '['
                    message = symbol + message + self.target[key][i]
                elif i == len(self.target[key]):
                    symbol = ']'
                    message = message + self.target[key][i] + symbol
                else:
                    symbol = ","
                    message = message + symbol + self.target[key][i]

            self.targetList[key] = message + tail
            message = head + message + "," + key + tail
            self.sendMessage(message)

    # 获取运动目标点列表
    def get_target_list(self):
        logger.info(self.targetList)
        return self.targetList

    # 设置初始目标点列表
    def set_init_target_List(self):
        head = "nav:set_flag_point"
        tail = "]"
        for key in self.initTarget:
            message = ""
            for i in range(len(self.initTarget[key])):
                self.initTarget[key][i] = str(self.initTarget[key][i])
                if i == 0:
                    symbol = '['
                    message = symbol + message + self.initTarget[key][i]
                elif i == len(self.initTarget[key]):
                    symbol = ']'
                    message = message + self.initTarget[key][i] + symbol
                else:
                    symbol = ","
                    message = message + symbol + self.initTarget[key][i]

            self.initTargetList[key] = message + tail
            message = head + message + "," + key + tail
            self.sendMessage(message)

    # 获取初始目标点列表
    def get_init_target_list(self):
        logger.info(self.initTargetList)
        return self.initTargetList

    def __new__(cls, *args, **kwargs):
        if not hasattr(Serial, "_instance"):
            with Serial._instance_lock:
                if not hasattr(Serial, "_instance"):
                    Serial._instance = object.__new__(cls)
        return Serial._instance

    # 重启机器
    def reboot_machine(self):
        logger.info("导航机器人 -----> 底盘重启")
        self.sendMessage('sys:reboot_machine')

    # WIFI IP(主机IP)
    def wifiIp(self):
        self.sendMessage('ip:request')

    # lan IP
    def lanIp(self):
        self.sendMessage("ip_lan:request")

    # 连接WIFI
    def connectWifi(self):
        self.sendMessage('connect_wifi[moja-5G{0}moja1122]'.format(chr(0x7f)))

    # 获取可用串口列表
    def getAvailableSerialList(self):
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            logger.info("The Serial port can't find!")
        else:
            if 0:
                plist_0 = list(plist[0])
                serialName = plist_0[0]
            else:
                serialName = "COM13"
            self.serialFd = serial.Serial(serialName, 115200, timeout=60)
            logger.info("check which port was really used >" + self.serialFd.name)

    # 发送串口信息
    def sendMessage(self, Data):
        # 将字符串数据转换为bytes数组
        # 数据包头
        frameHead = "AA54"
        # 数据体长度
        dataLen = "{0:02x}".format(len(Data))
        # 数据体
        dataBody = bytes(Data, encoding="ascii")
        # 校验位
        parity = "{0:02x}".format(parityBit(Data))
        # 串口通信数据
        message = binascii.a2b_hex(frameHead + dataLen) + dataBody + binascii.a2b_hex(parity)
        serStr = self.serialFd.write(message)
        # print(serStr)

    # 接收串口信息
    def recvMessage(self):
        if self.serialFd.in_waiting:
            with open("serialLog.txt", "a") as f:
                serStr = str(self.serialFd.read(self.serialFd.in_waiting)) + "\r\n"
                f.write(serStr)
                # if "move_status" in serStr:
                #     print("move_status")
            serStr = serStr.replace("\\xaaT", "0xaaT")
            serStr = serStr.replace("\\", "0")
            serStrList = serStr.split("0xaaT")
            # del serStrList[0]
            # 解析有效数据
            for tempStr in serStrList:
                # 过滤无效数据
                # logger.info("接收数据> " + tempStr)
                if "move_status" in tempStr:
                    startIndex = tempStr.find("move_status")
                    logger.info("move_status: " + tempStr[startIndex + 12])
                    globalVariable.set_nav_status(tempStr[startIndex + 12])

                if "get_max_vel" in tempStr:
                    logger.info("Get Current Speed >" + tempStr)

                if "max_vel" in tempStr:
                    logger.info("Max Speed Set >" + tempStr)

                if "ip:" in tempStr:
                    logger.info("WIFI IP: " + tempStr[-2])

                if len(tempStr) >= 4 and tempStr[:2] == '0x':
                    dataAvailableLen = int(tempStr[:4], 16)

                    if "lase" not in tempStr and "ver:" not in tempStr:
                        self.availableDataList.append(tempStr[4:4+dataAvailableLen])
                        logger.info(tempStr[4:4+dataAvailableLen])
                    else:
                        pass

                    if "nav:pose" in tempStr:
                        logger.info("当前位置信息: " + self.availableDataList[-1])
                        logger.info("nav:pose> " + self.availableDataList[-1][8:])
                        if "]" in self.availableDataList[-1][8:]:
                            globalVariable.angle = self.availableDataList[-1].replace("[", "").replace("]", "").split(",")[2]
                            print(globalVariable.angle)
                            self.availableDataList = []
                    elif "set_flag_point" in tempStr:
                        logger.info("给定目标点名称导航: " + self.availableDataList[-1])
                    elif "point" in tempStr:
                        logger.info("设置标定点: " + self.availableDataList[-1])
                    elif "wifi" in tempStr:
                        logger.info("导航主机连接WIFI: " + self.availableDataList[-1])
                    elif "ip_lan" in tempStr:
                        logger.info("网口 IP: " + self.availableDataList[-1])
                    elif "move_status" in tempStr:
                        logger.info("机器人导航状态: " + self.availableDataList[-1])
                    else:
                        # print("没有请求的数据返回")
                        pass
                else:
                    pass
            del serStrList
        else:
            # print("self.serialFd.in_waiting>" + str(self.serialFd.in_waiting))
            pass

    # 关闭串口
    def serialClose(self):
        self.serialFd.close()

    # 获取机器人当前位置
    def getPose(self):
        self.sendMessage("nav:get_pose")

    # 获取当前最大速度
    def getMaxVel(self):
        self.sendMessage("get_max_vel")

    # 修改最大速度
    def modifyMaxVel(self, speed):
        self.sendMessage("max_vel[{0}]".format(speed))

    # 直接对接充电桩
    def justCharge(self):
        self.sendMessage("goal:just_charge")

    # 取消导航
    def cancelGuide(self):
        self.sendMessage("cancel_goal")

    # 移动机器人
    def moveRobot(self, distance, angle, speed):
        self.sendMessage("move[{0},{1},{2}]".format(distance, angle, speed))

    # 获取某个标定点位置信息
    def getSetTargetPoint(self, targetName):
        self.sendMessage("nav:get_flag_point{0}".format(targetName))

    def powerOn(self):
        self.sendMessage("sys:lock")
