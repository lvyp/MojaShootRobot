# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : main.py
# @Software: PyCharm

import threading
from loggerMode import logger
from dualRobotInteractionMode import dualRobotInteractionMode
from mapRouteSettingMode import mapRouteSettingMode
from positionInformationFromChassisMode import positionInformationFromChassisMode
from scoreMode import scoreMode
import globalVariable


def sensorCount():
    while 1:
        # 进行计数通信
        scoreFlag = globalVariable.sensorCount.getPortVal()
        if scoreFlag:
            globalVariable.blueScore += 1
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
    logger.info("墨甲导览机器人启动入口")
    globalVariable._init()

    # 设置初始点运动位置
    # globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_init_target_list())
    # globalVariable.set_value("mapRouteSettingInitPointFlag", True)

    globalVariable.set_value("actionFlag", False)
    globalVariable.set_value("mapRouteSettingFlag", False)
    globalVariable.set_value("positionInformationFromChassisFlag", False)
    globalVariable.set_value("positionInformationFromChassisInitPointFlag", False)

    # 设置线程组
    threads = []

    # 创建线程：
    # actionControl = threading.Thread(target=actionControlMode)
    lora = threading.Thread(target=loraSerial)
    sensor = threading.Thread(target=sensorCount)
    score = threading.Thread(target=scoreMode)
    # tcpServer = threading.Thread(target=serverMode)
    dualRobotInteraction = threading.Thread(target=dualRobotInteractionMode)
    mapRouteSetting = threading.Thread(target=mapRouteSettingMode)
    # speechRecognition = threading.Thread(target=speechRecognitionMode)
    positionInformationFromChassis = threading.Thread(target=positionInformationFromChassisMode)
    # speechRecognition.setName("speechRecognition")
    # actionControl.setName("actionControl")
    lora.setName("lora")
    sensor.setName("sensor")
    score.setName("score")
    # tcpServer.setName("tcpServer")
    dualRobotInteraction.setName("dualRobotInteraction")
    mapRouteSetting.setName("mapRouteSetting")
    positionInformationFromChassis.setName("positionInformationFromChassis")

    # remoteControl = threading.Thread(target=remoteControlMode)
    # accessSystemUpdateRegularly = threading.Thread(target=accessSystemUpdateRegularlyMode)
    # remoteControl.setName("remoteControl")
    # accessSystemUpdateRegularly.setName("accessSystemUpdateRegularly")

    # 添加到线程组
    # threads.append(speechRecognition)
    # threads.append(actionControl)
    threads.append(lora)
    threads.append(sensor)
    threads.append(score)
    # threads.append(tcpServer)
    threads.append(mapRouteSetting)
    threads.append(dualRobotInteraction)
    threads.append(positionInformationFromChassis)
    # threads.append(remoteControl)
    # threads.append(accessSystemUpdateRegularly)

    # 开启线程
    for thread in threads:
        thread.start()

    # 线程阻塞
    for thread in threads:
        thread.join()
