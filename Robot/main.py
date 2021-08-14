# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : main.py
# @Software: PyCharm

import threading
import time

from loggerMode import logger
from dualRobotInteractionMode import dualRobotInteractionMode
from mapRouteSettingMode import mapRouteSettingMode
from positionInformationFromChassisMode import positionInformationFromChassisMode
from scoreMode import scoreMode
import globalVariable
from tcpClient import tcpWeb


def sensorCount():
    while 1:
        # 进行计数通信
        scoreFlag = globalVariable.sensorCount.getPortVal()
        # print("进行计数通信")
        if scoreFlag:
            globalVariable.blueScore += 1
            print(str(globalVariable.blueScore))
            time.sleep(0.2)
        else:
            pass


def loraSerial():
    while 1:
        globalVariable.loraSerial.loraRecvMessage()


def serverMode():
    while 1:
        globalVariable.shootRobotServer.recvMessage()


if __name__ == '__main__':
    # 墨甲导览机器人启动入口
    logger.info("墨甲射击机器人启动入口")
    globalVariable._init()

    globalVariable.set_value("scoreFlag", True)
    globalVariable.set_value("actionFlag", False)
    globalVariable.set_value("mapRouteSettingFlag", False)
    globalVariable.set_value("positionInformationFromChassisFlag", False)
    globalVariable.set_value("positionInformationFromChassisInitPointFlag", False)

    # 设置线程组
    threads = []

    # 创建线程：
    lora = threading.Thread(target=loraSerial)
    sensor = threading.Thread(target=sensorCount)
    score = threading.Thread(target=scoreMode)
    # tcpServer = threading.Thread(target=serverMode)
    dualRobotInteraction = threading.Thread(target=dualRobotInteractionMode)
    mapRouteSetting = threading.Thread(target=mapRouteSettingMode)
    positionInformationFromChassis = threading.Thread(target=positionInformationFromChassisMode)
    tcpClient = threading.Thread(target=tcpWeb)
    
    lora.setName("lora")
    sensor.setName("sensor")
    score.setName("score")
    tcpClient.setName("tcpClient")
    # tcpServer.setName("tcpServer")
    dualRobotInteraction.setName("dualRobotInteraction")
    mapRouteSetting.setName("mapRouteSetting")
    positionInformationFromChassis.setName("positionInformationFromChassis")


    # 添加到线程组
    threads.append(lora)
    threads.append(sensor)
    threads.append(score)
    threads.append(tcpClient)
    # threads.append(tcpServer)
    threads.append(mapRouteSetting)
    threads.append(dualRobotInteraction)
    threads.append(positionInformationFromChassis)

    # 开启线程
    for thread in threads:
        thread.start()

    # 线程阻塞
    for thread in threads:
        thread.join()
