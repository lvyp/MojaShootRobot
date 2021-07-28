# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : main.py
# @Software: PyCharm

import threading
from loggerMode import logger
from speechRecognitionMode import speechRecognitionMode
from actionControlMode import actionControlMode
from dualRobotInteractionMode import dualRobotInteractionMode
from mapRouteSettingMode import mapRouteSettingMode
from positionInformationFromChassisMode import positionInformationFromChassisMode
from remoteControlMode import remoteControlMode
from accessSystemUpdateRegularlyMode import accessSystemUpdateRegularlyMode
import globalVariable

if __name__ == '__main__':
    # 墨甲导览机器人启动入口
    logger.info("墨甲导览机器人启动入口")
    globalVariable._init()

    globalVariable.set_value("actionFlag", False)
    globalVariable.set_value("mapRouteSettingFlag", False)
    globalVariable.set_value("positionInformationFromChassisFlag", False)

    # 设置线程组
    threads = []

    # 创建线程：
    # actionControl = threading.Thread(target=actionControlMode)
    dualRobotInteraction = threading.Thread(target=dualRobotInteractionMode)
    mapRouteSetting = threading.Thread(target=mapRouteSettingMode)
    speechRecognition = threading.Thread(target=speechRecognitionMode)
    positionInformationFromChassis = threading.Thread(target=positionInformationFromChassisMode)
    speechRecognition.setName("speechRecognition")
    # actionControl.setName("actionControl")
    dualRobotInteraction.setName("dualRobotInteraction")
    mapRouteSetting.setName("mapRouteSetting")
    positionInformationFromChassis.setName("positionInformationFromChassis")

    # remoteControl = threading.Thread(target=remoteControlMode)
    # accessSystemUpdateRegularly = threading.Thread(target=accessSystemUpdateRegularlyMode)
    # remoteControl.setName("remoteControl")
    # accessSystemUpdateRegularly.setName("accessSystemUpdateRegularly")

    # 添加到线程组
    threads.append(speechRecognition)
    # threads.append(actionControl)
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
