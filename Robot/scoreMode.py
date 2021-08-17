# -*- coding: utf-8 -*-
# @Time : 2021/7/29 14:01
# @Author :
# @Site : Beijing
# @File : scoreMode.py
# @Software: PyCharm
import time

import globalVariable
from actionMode import action
from loggerMode import logger
import threading
from MoJaTimer import *


def robotStatus(comMotor, canMotor):
    # 计算总积分
    sumScore = globalVariable.blueScore

    # 得分将本次得分值赋值给上一次得分值
    globalVariable.lastScore = sumScore

    # 计算游戏时间
    currentTime = timerMachine()
    if globalVariable.initTime == 0:
        globalVariable.initTime = currentTime
    # 根据得分不同进行不同状态变化
    if ((sumScore == 10) or (currentTime - globalVariable.initTime >= 60)) \
            and (globalVariable.simple_count == 0):
        # 播报次数设置:1,播报一次之后不再进行播报
        globalVariable.simple_count = 1
        # 表情
        action(comMotor, canMotor, "happy")
        # 对话播放
        print("simple_plot\n")
        globalVariable.set_value("simple_plot", True)
    elif ((sumScore == 30) or (currentTime - globalVariable.initTime >= 120)) \
            and (globalVariable.easy_count == 0):
        # 播报次数设置:1,播报一次之后不再进行播报
        globalVariable.easy_count = 1
        # 表情
        action(globalVariable.get_comMotor(), globalVariable.get_canMotor(), "embarrassed")
        # 提升底盘速度
        globalVariable.mojaSerial.modifyMaxVel("0.6")
        # 对话播放
        print("easy_plot\n")
        globalVariable.set_value("easy_plot", True)
    elif ((sumScore == 70) or (currentTime - globalVariable.initTime >= 180)) \
            and (globalVariable.hard_count == 0):
        # 播报次数设置:1,播报一次之后不再进行播报
        globalVariable.hard_count = 1
        # 表情
        action(globalVariable.get_comMotor(), globalVariable.get_canMotor(), "anger")
        # 提升底盘速度
        globalVariable.mojaSerial.modifyMaxVel("1.0")
        # 对话播放
        globalVariable.set_value("hard_plot", True)
    elif (sumScore == 100) or (currentTime - globalVariable.initTime >= 240):
        globalVariable.set_value("scoreFlag", False)
        # 将底盘运动速度降低
        globalVariable.mojaSerial.modifyMaxVel("0.3")
        # 表情
        action(globalVariable.get_comMotor(), globalVariable.get_canMotor(), "init")
        # 让机器人回到初始位置进行两点运动
        globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_init_target_list())
        globalVariable.set_value("mapRouteSettingFlag", False)
        globalVariable.set_value("mapRouteSettingInitPointFlag", True)
        # 游戏结束，得分状态清空
        globalVariable.lastScore = 0
        globalVariable.redScore = 0
        globalVariable.yellowScore = 0
        globalVariable.blueScore = 0
        # 播报次数设置为初始值：0
        globalVariable.simple_count = 0
        globalVariable.easy_count = 0
        globalVariable.hard_count = 0
        # 初始时间设置为0
        globalVariable.initTime = 0
    else:
        pass


def scoreMode():
    logger.info("得分模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    comMotor = globalVariable.get_comMotor()
    canMotor = globalVariable.get_canMotor()
    while 1:
        rLock.acquire()
        if globalVariable.get_value("scoreFlag"):
            # print("lastScore>" + str(globalVariable.lastScore))
            # print("blueScore>" + str(globalVariable.blueScore))
            if globalVariable.get_value("first_start"):
                globalVariable.blueScore = 0
                globalVariable.loraSerial.modbusRtuSendMessage(globalVariable.blueScore)
                globalVariable.set_value("first_start", False)
            # 判断是否得分，得分通过modbus rtu控制得分牌显示得分
            if globalVariable.lastScore == globalVariable.blueScore:
                pass
            else:
                globalVariable.loraSerial.modbusRtuSendMessage(globalVariable.blueScore)

            # 机器人状态变化
            robotStatus(comMotor, canMotor)
        else:
            pass

        event.set()
        rLock.release()
