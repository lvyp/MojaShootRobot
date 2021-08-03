# -*- coding: utf-8 -*-

import threading
from enum import Enum
from serialClass import Serial
from buttonTcpServer import *
import random


def _init():  # 初始化
    global _global_dict
    global _event
    global _position_name_list
    global position_name
    global GlobalHttp
    global _position_list_len
    global _navStatus
    global mojaSerial
    global session_id
    global moveStatus
    global initPoint
    # 红黄蓝得分
    global redScore
    global yellowScore
    global blueScore
    # 播报次数
    global simple_count
    global easy_count
    global hard_count
    global shootRobotServer


    _global_dict = {}
    _event = threading.Event()
    _position_name_list = []
    position_name = ""
    _position_list_len = 0
    _navStatus = "0"
    session_id = ""
    mojaSerial = Serial()
    moveStatus = 0  # 0是未运动;1是运动中;
    initPoint = []
    redScore = 0
    yellowScore = 0
    blueScore = 0
    simple_count = 0
    easy_count = 0
    hard_count = 0
    shootRobotServer = TcpServer()


def get_nav_status():
    return _navStatus


def set_nav_status(currentStatus):
    global _navStatus
    _navStatus = currentStatus


def get_position_list_len():
    return _position_list_len


def get_position_name():
    global position_name
    while 1:
        randomPosition = random.sample(_position_name_list, len(_position_name_list))
        if position_name != randomPosition:
            position_name = randomPosition
            break
        else:
            pass
    return position_name


def set_position_name_by_serial(serial_list):
    for key in serial_list:
        _position_name_list.append(key)


def set_position_name():
    for key in GlobalHttp.get_target_list():
        _position_name_list.append(key)


def get_position_list():
    return GlobalHttp.get_target_list()


def set_value(key, value):
    """ 定义一个全局变量 """
    _global_dict[key] = value


def get_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        return defValue


def get_event():
    return _event
