# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : mapRouteSettingMode.py
# @Software: PyCharm

import threading
import globalVariable
from loggerMode import logger
from serialClass import Serial


def mapRouteSettingMode():
    # 地图路线设置模块：发送目的地位置给底层（底盘）
    logger.info("地图路线设置模块入口")
    event = globalVariable.get_event()
    rLock = threading.RLock()
    while 1:
        # logger.info("线程：" + threading.current_thread().name + " Id:" + str(threading.get_ident()))
        event.wait()
        rLock.acquire()
        if globalVariable.get_value("mapRouteSettingFlag") is True:
            logger.info("地图设置向模块底层发送数据")
            # globalVariable.set_position_name_by_serial(globalVariable.mojaSerial.get_target_list())
            globalVariable.mojaSerial.sendMessage("point[{0}]".format(globalVariable.get_position_name()))
            globalVariable.moveStatus = 1  # 设置机器人运动状态为运动中，运动中不会进行声源定位
            globalVariable.set_value("positionInformationFromChassisFlag", True)
            globalVariable.set_value("mapRouteSettingFlag", False)
        elif globalVariable.get_value("mapRouteSettingInitPointFlag") is True:
            # globalVariable.mojaSerial.sendMessage("nav:get_pose")
            # 退回到充电桩位置
            globalVariable.mojaSerial.sendMessage("point[charging_pile]")
            # 直接对接充电桩充电
            globalVariable.mojaSerial.justCharge()
            globalVariable.moveStatus = 1  # 设置机器人运动状态为运动中，运动中不会进行声源定位
            globalVariable.set_value("mapRouteSettingInitPointFlag", False)
            globalVariable.set_value("positionInformationFromChassisInitPointFlag", True)
        else:
            # logger.info("什么都不做")
            pass
        # 代码实现部分
        # 代码实现部分
        rLock.release()
        event.clear()
