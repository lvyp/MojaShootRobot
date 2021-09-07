# -*- coding: utf-8 -*-
# @Time : 2021/6/18 16:12
# @Author :
# @Site : Beijing
# @File : positionInformationFromChassisMode.py
# @Software: PyCharm

import threading

from playsound import playsound
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
    globalVariable.mojaSerial.recvMessage()
    # print("recvMessage>" + globalVariable.get_nav_status())
    if globalVariable.get_nav_status() == "2":
        if settingFlag == "mapRouteSettingInitPointFlag":
            globalVariable.set_value(settingFlag, False)
            # 充电桩重定位
            print("充电桩重定位")
            globalVariable.mojaSerial.reloc(globalVariable.position_name)
        else:
            print("到达指定点位进行重定位")
            globalVariable.get_position_XYZ_by_name(globalVariable.position_name)
            globalVariable.set_value(settingFlag, True)
        globalVariable.set_value(flag, False)
        globalVariable.set_nav_status("0")
    elif globalVariable.get_nav_status() == "4":
        logger.info("有阻碍物！！！")
        globalVariable.set_nav_status("0")
    elif globalVariable.get_nav_status() == "5":
        logger.info("有阻碍物！！！")
        globalVariable.set_nav_status("0")
    elif globalVariable.get_nav_status() == "'":
        globalVariable.set_value(flag, False)
        globalVariable.set_value(settingFlag, True)
        globalVariable.set_nav_status("0")
    elif globalVariable.get_nav_status() == "0":
        pass
    else:
        print("getPositionAndStartPlot >> globalVariable.get_nav_status()=" + str(globalVariable.get_nav_status()))
        globalVariable.set_value(flag, False)
        globalVariable.set_value(settingFlag, True)
        globalVariable.set_nav_status("0")
    # print("recvMessage> out!!")


def positionInformationFromChassisMode():
    # 底盘交互模块：底盘实时交互获取位置信息。到达固定地点则进行剧本表演
    logger.info("底盘交互模块模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        try:
            # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
            rLock.acquire()
            # 获取位置信息被触发才会从底层获取当前位置信息
            if globalVariable.get_value("positionInformationFromChassisFlag"):
                # logger.info("底盘交互模块底层发送数据：实时获取位置信息")
                getPositionAndStartPlot("positionInformationFromChassisFlag", "mapRouteSettingFlag")
            elif globalVariable.get_value("positionInformationFromChassisInitPointFlag"):
                getPositionAndStartPlot("positionInformationFromChassisInitPointFlag", "mapRouteSettingInitPointFlag")
            else:
                # logger.info("什么都不做")
                pass
            event.set()
            rLock.release()
        except Exception as e:
            print("positionInformationFromChassisMode >> " + str(e))


if __name__ == "__main__":
    globalVariable._init()
    globalVariable.set_value("positionInformationFromChassisFlag", True)
    positionInformationFromChassisMode()
