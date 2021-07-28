# -*- coding: utf-8 -*-

import threading
from enum import Enum
from serialClass import Serial


def _init():  # 初始化
    global _global_dict
    global _event
    global _intent
    global _slot
    global _position
    global _position_name_list
    global position_name
    global GlobalHttp
    global _position_list_len
    global _navStatus
    global mojaSerial
    global session_id
    global moveStatus
    global initPoint

    _global_dict = {}
    _event = threading.Event()
    _intent = IntentEnum.INITIALACTION
    _slot = {'position': SlotPositionEnum.ALL, 'direction': SlotDirectionEnum.UP}
    _position = {"positionA": False, "positionB": False,
                 "positionC": False, "positionD": False}
    _position_name_list = []
    position_name = ""
    _position_list_len = 0
    _navStatus = "0"
    session_id = ""
    mojaSerial = Serial()
    moveStatus = 0  # 0是未运动;1是运动中;
    initPoint = []


def get_nav_status():
    return _navStatus


def set_nav_status(currentStatus):
    global _navStatus
    _navStatus = currentStatus


def get_position_list_len():
    return _position_list_len


def get_position_name():
    global position_name
    global _position_list_len
    position_name = _position_name_list[0]
    del _position_name_list[0]
    _position_list_len = len(_position_name_list)
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


def set_position(key, value):
    _position[key] = value


def get_position(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _position[key]
    except KeyError:
        return defValue


class IntentEnum(Enum):
    INITIALACTION = 0  # 初始状态
    HEADACTION = 1  # 头部动作
    EYEACTION = 2  # 眼部动作
    MOUTHACTION = 3  # 嘴部动作
    MAPNAVIGATION = 4  # 地图导览
    TTSBROADCAST = 5  # TTS播报


class SlotPositionEnum(Enum):
    ALL = 0
    LEFT = 1
    RIGHT = 2


class SlotDirectionEnum(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
