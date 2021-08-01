# -*- coding: utf-8 -*-
# @Time : 2021/7/29 14:01
# @Author :
# @Site : Beijing
# @File : scoreMode.py
# @Software: PyCharm
import globalVariable
import dualRobotInteractionMode
from loggerMode import logger
import threading


def robotStatus():
    # 计算总积分
    sumScore = globalVariable.redScore + globalVariable.yellowScore + globalVariable.blueScore

    # 根据得分不同进行不同状态变化
    if (sumScore == 0) and (globalVariable.simple_count == 0):
        # 播报次数设置:1,播报一次之后不再进行播报
        globalVariable.simple_count == 1
        # 对话播放
        globalVariable.set_position("simple_plot", True)
    elif (sumScore == 30) and (globalVariable.easy_count == 0):
        # 播报次数设置:1,播报一次之后不再进行播报
        globalVariable.easy_count == 1
        # 提升底盘速度
        globalVariable.mojaSerial.modifyMaxVel("0.6")
        # 对话播放
        globalVariable.set_position("easy_plot", True)
    elif (sumScore == 70) and (globalVariable.hard_count == 0):
        # 播报次数设置:1,播报一次之后不再进行播报
        globalVariable.hard_count == 1
        # 提升底盘速度
        globalVariable.mojaSerial.modifyMaxVel("1.0")
        # 对话播放
        globalVariable.set_position("hard_plot", True)
    elif sumScore == 100:
        # 将底盘运动速度降低
        globalVariable.mojaSerial.modifyMaxVel("0.3")
        # 运动状态置位，未运动
        globalVariable.moveStatus = 0
        # 让机器人回到充电桩处并充电
        globalVariable.set_value("mapRouteSettingInitPointFlag", True)
        # 游戏结束，得分状态清空
        globalVariable.redScore = 0
        globalVariable.yellowScore = 0
        globalVariable.blueScore = 0
        # 播报次数设置为初始值：0
        globalVariable.simple_count = 0
        globalVariable.easy_count = 0
        globalVariable.hard_count = 0
    else:
        pass


def scoreMode():
    logger.info("得分模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        rLock.acquire()
        if globalVariable.get_value("scoreFlag") is True:
            # 进行计数通信

            # 根据不同小球的得分发送相应的数据进行显示

            # 机器人状态变化
            robotStatus()
        else:
            pass

        event.set()
        rLock.release()


