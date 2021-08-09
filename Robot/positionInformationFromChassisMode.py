# -*- coding: utf-8 -*-
# @Time : 2021/6/18 16:12
# @Author :
# @Site : Beijing
# @File : positionInformationFromChassisMode.py
# @Software: PyCharm

import math
import threading

from playsound import playsound
from serialClass import Serial
import globalVariable
from loggerMode import logger

TTS_BY_OBSTRUCTION_PATH = "./TtsRecording/Obstruction/"


def PlayVoice(path):
    # print(path)
    playJudge = playsound(path, True)  # 设置为True需要同步进行。否则录音时会将播放的应该回复录入
    if playJudge is False:
        logger.info("音频格式不正确，无法播放！！\n")
    else:
        logger.info("对话应答已回复！！\n")


def getPositionAndStartPlot(flag, settingFlag):
    # 请求获取当前位置信息
    globalVariable.mojaSerial.getPose()
    globalVariable.mojaSerial.recvMessage()
    if globalVariable.get_nav_status() == "2":
        globalVariable.set_value(flag, False)
        globalVariable.set_value(settingFlag, True)
    elif globalVariable.get_nav_status() == "4":
        logger.info("有阻碍物！！！")
    elif globalVariable.get_nav_status() == "5":
        logger.info("有阻碍物！！！")
    else:
        pass
    globalVariable.set_nav_status("0")


def positionInformationFromChassisMode():
    # 底盘交互模块：底盘实时交互获取位置信息。到达固定地点则进行剧本表演
    logger.info("底盘交互模块模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        rLock.acquire()
        # 获取位置信息被触发才会从底层获取当前位置信息
        if globalVariable.get_value("positionInformationFromChassisFlag") is True:
            # logger.info("底盘交互模块底层发送数据：实时获取位置信息")
            getPositionAndStartPlot("positionInformationFromChassisFlag", "mapRouteSettingFlag")
        elif globalVariable.get_value("positionInformationFromChassisInitPointFlag") is True:
            getPositionAndStartPlot("positionInformationFromChassisInitPointFlag", "mapRouteSettingInitPointFlag")
        else:
            # logger.info("什么都不做")
            pass
        event.set()
        rLock.release()
