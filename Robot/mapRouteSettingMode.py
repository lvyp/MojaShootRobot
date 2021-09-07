# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : mapRouteSettingMode.py
# @Software: PyCharm

import threading
import globalVariable
from loggerMode import logger


def mapRouteSettingMode():
    # 地图路线设置模块：发送目的地位置给底层（底盘）
    logger.info("地图路线设置模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        try:
            # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
            event.wait()
            rLock.acquire()
            if globalVariable.get_value("mapRouteSettingFlag") is True:
                logger.info("游戏开始>>>地图设置向模块底层发送数据")
                # 取消初始位置运动导航
                globalVariable.mojaSerial.cancelGuide()
                # 发送游戏点位位置名称
                # if globalVariable.blueScore < 8:
                #     if globalVariable.currentPosNum == 2:
                #         globalVariable.currentPosNum = 0
                # elif (globalVariable.blueScore >= 8) and (globalVariable.blueScore < 16):
                #     if globalVariable.currentPosNum == 0:
                #         globalVariable.currentPosNum = 2
                #     elif globalVariable.currentPosNum == 1:
                #         globalVariable.currentPosNum = 0
                #     elif globalVariable.currentPosNum == 4:
                #         globalVariable.currentPosNum = 2
                #     else:
                #         pass
                # else:
                #     if globalVariable.currentPosNum == 2:
                #         globalVariable.currentPosNum = 4
                #     elif globalVariable.currentPosNum == 3:
                #         globalVariable.currentPosNum = 2
                #     elif globalVariable.currentPosNum == 6:
                #         globalVariable.currentPosNum = 4
                #     else:
                #         pass
                goal_postion = globalVariable.get_position_name()
                globalVariable.mojaSerial.sendMessage("point[{0}]".format(goal_postion))
                print("point[{0}]".format(goal_postion))
                globalVariable.set_value("positionInformationFromChassisFlag", True)
                globalVariable.set_value("mapRouteSettingFlag", False)

            elif globalVariable.get_value("mapRouteSettingInitPointFlag") is True:
                logger.info("游戏结束>>>地图设置向模块底层发送数据")
                # 取消初始位置运动导航
                globalVariable.mojaSerial.cancelGuide()
                # 初始位置固定点位进行移动
                goal_postion = globalVariable.get_position_name()
                globalVariable.mojaSerial.sendMessage("point[{0}]".format(goal_postion))
                # 导航到充电桩并充电
                # globalVariable.mojaSerial.pointCharge(goal_postion)
                print("point[{0}]".format(goal_postion))
                # # 退回到充电桩位置
                # globalVariable.mojaSerial.sendMessage("point[charging_pile]")
                # # 直接对接充电桩充电
                # globalVariable.mojaSerial.justCharge()
                globalVariable.set_value("mapRouteSettingInitPointFlag", False)
                globalVariable.set_value("positionInformationFromChassisInitPointFlag", True)
            else:
                # logger.info("什么都不做")
                pass
            # 代码实现部分
            # 代码实现部分
            rLock.release()
            event.clear()
        except Exception as e:
            print("mapRouteSettingMode >> " + str(e))
