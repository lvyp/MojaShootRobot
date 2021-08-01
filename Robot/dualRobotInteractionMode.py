# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : dualRobotInteractionMode.py
# @Software: PyCharm
import math
import os
import time
import datetime
import json
import threading
import globalVariable
from loggerMode import logger
from playsound import playsound
import playAudioByLeftRightTrack as LRTrack

TTS_BY_COMMUNICATION_PATH = "./TtsRecording/dualRobotCommunication/"
TTS_BY_XIANGSHENG_PATH = "./TtsRecording/xiangsheng/"


def PlayVoice(path):
    # print(path)
    playJudge = playsound(path, False)  # 设置为True需要同步进行。否则录音时会将播放的应该回复录入
    if playJudge is False:
        logger.info("音频格式不正确，无法播放！！\n")
    else:
        logger.info("对话应答已回复！！\n")


def minChangeToSec(h, m, s):
    s = h*60*60 + m*60 + s
    return s


def timerMachine(startTime=0.000):
    dt_hms = datetime.datetime.now().strftime('%H:%M:%S.%f')
    h, m, s = dt_hms.strip().split(":")
    hms = minChangeToSec(float(h), float(m), float(s))
    # print("m: " + m + " s: " + s + " ms: " + str(ms) + " startTime: " + str(startTime))
    return float('%.3f' % (hms - startTime))


def parsePlot(jsonPath):
    with open(jsonPath, "r", encoding="utf-8") as f:
        plotDict = json.load(f)
        plotList = plotDict["MoJa"]
        f.close()

    startTime = timerMachine()
    # 获取列表中所有字典数据
    for plot in plotList:
        # 判断字典数据时间点
        tempDict = {"time": plot["time"],
                    "sub_time_child": plot["sub_time_child"],
                    "sub_time_old": plot["sub_time_old"]}
        timeFlag = 0
        childTimeFlag = 0
        oldTimeFlag = 0
        print(plot["dialogue"])
        while True:
            currentTime = timerMachine(startTime)

            currentHuman = plot["current_human"]

            if plot["sub_time_child"] == 0 and childTimeFlag == 0:
                childTimeFlag += 1
                del tempDict["sub_time_child"]
            if plot["sub_time_old"] == 0 and oldTimeFlag == 0:
                oldTimeFlag += 1
                del tempDict["sub_time_old"]

            # print(currentTime)
            # if math.isclose(plot["time"], currentTime, abs_tol=0.010) and timeFlag == 0:
            if plot["time"] <= currentTime and timeFlag == 0:
                timeFlag += 1
                del tempDict["time"]
                if plot["dialogue"] != "":
                    # PlayVoice(plot["dialogue"])
                    LRTrack.get_audio_devices_all_msg_dict(plot["dialogue"], currentHuman)
            # if math.isclose(plot["sub_time_child"], currentTime, abs_tol=0.010) and childTimeFlag == 0:
            if plot["sub_time_child"] <= currentTime and childTimeFlag == 0:
                childTimeFlag += 1
                del tempDict["sub_time_child"]
                if plot["action_child"] != "":
                    print("action_child")
            # if math.isclose(plot["sub_time_old"], currentTime, abs_tol=0.010) and oldTimeFlag == 0:
            if plot["sub_time_old"] <= currentTime and oldTimeFlag == 0:
                oldTimeFlag += 1
                del tempDict["sub_time_old"]
                if plot["action_old"] != "":
                    print("action_old")

            if len(tempDict) == 0:
                print("len(tempDict): " + str(len(tempDict)))
                break
            else:
                # print(currentTime)
                # print(tempDict)
                pass


def mapRouteSettingClearJudge():
    if globalVariable.get_position_list_len() > 0:
        # 位置列表不为空，继续发送位置信息
        globalVariable.set_value("mapRouteSettingFlag", True)
    else:
        # 位置列为空，不发送位置信息
        # 运动状态置位，未运动
        globalVariable.moveStatus = 0
        # 让机器人回到初始点
        globalVariable.set_value("mapRouteSettingInitPointFlag", True)


def switch_if():
    if globalVariable.get_position(globalVariable.position_name):
        logger.info("到达位置:" + globalVariable.position_name)
        jsonFilePath = "./PLOT/" + globalVariable.position_name + ".json"

        if os.path.exists(jsonFilePath):
            parsePlot(jsonFilePath)
            globalVariable.set_position(globalVariable.position_name, False)
            mapRouteSettingClearJudge()
        else:
            globalVariable.set_position(globalVariable.position_name, False)
            mapRouteSettingClearJudge()


def dualRobotInteractionMode():
    # 双机器人互动模块：设置对话情景，根据机器人对话情景，发送相应的指令到动作模块
    logger.info("双机器人互动模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        event.wait()
        rLock.acquire()
        # 代码实现部分
        switch_if()
        # 代码实现部分
        rLock.release()
        event.clear()
