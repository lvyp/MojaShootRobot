# -*- coding: utf-8 -*-
import queue
from robotLed import RobotLedSerial

from loraSerialClass import LoraSerial
from serialClass import Serial
from buttonTcpServer import *
import random


def _init():  # 初始化
    global _global_dict
    global _event
    global _position_name_list
    global _position_name_dict
    global position_name
    global _navStatus
    global mojaSerial
    global session_id
    global currentPosNum
    global initPoint
    #第一次
    global fisrt_bgm
    # 上次得分
    global lastScore
    # 红黄蓝得分
    global redScore
    global yellowScore
    global blueScore
    # 播报次数
    global simple_count
    global easy_count
    global hard_count
    global shootRobotServer
    # 计时初始值
    global initTime
    # 计分实例
    global sensorCount
    # Lora通信实例
    global loraSerial
    # 运动旋转角度
    global angle
    # can通信
    global canMotor
    # com通信
    global comMotor
    # 进程同步变量 --> 传感器
    global syn
    # lora字符串拼接
    global m_str
    # 进程同步变量 --> 表情
    global m_express
    # playVideoByPyGame 播放音频变量
    global playFlag
    # 播放音频名
    global talk_1
    # 获取不到地盘数据的当前时间
    global currentTime
    # 获取不到地盘数据的上一次时间
    global lastTime
    # lora接收数据开始变量标志位[0]与结束变量标志位[1]
    global loraRecvFlag
    # 得分模块不进球计时
    global lastShootOutTime
    # LED队列
    global ledQueue
    # 机器人上LED
    global robotLed
    # lora重发计数
    global loraErrorNumber
    # 眼睛屏幕队列
    global queEye

    _global_dict = {}
    _event = threading.Event()
    _position_name_list = []
    _position_name_dict = {}
    position_name = ""
    _position_list_len = 0
    _navStatus = "0"
    session_id = ""
    currentPosNum = 0  # 计算地点位置数
    initPoint = []
    lastScore = 0
    redScore = 0
    yellowScore = 0
    blueScore = 0
    simple_count = 0
    easy_count = 0
    hard_count = 0
    initTime = 0
    angle = 0
    syn = 0
    m_str = ""
    m_express = {"bgm": "./tts/bgm/BGM.wav"}
    playFlag = False
    talk_1 = ""
    currentTime = 0
    lastTime = 0
    loraErrorNumber = 0
    loraRecvFlag = {"startFlag": False, "endFlag": False}
    lastShootOutTime = 0
    ledQueue = queue.Queue(1)
    queEye = queue.Queue(1)
    # sensorCount = SensorCount()
    if 1:
        mojaSerial = Serial()

    loraSerial = LoraSerial()
    robotLed = RobotLedSerial()
    # comMotor = ComMotor("COM1")
    # canMotor = CanMotor()
    # canMotor.RUN_CAN()
    # canMotor.MOTOR_INIT(16)
    # canMotor.MOTOR_INIT(17)
    # canMotor.MOTOR_INIT(18)
    # shootRobotServer = TcpServer()


def get_comMotor():
    return comMotor


def get_canMotor():
    return canMotor


def get_nav_status():
    return _navStatus


def set_nav_status(currentStatus):
    global _navStatus
    _navStatus = currentStatus


# 随机获取标定点名称
def get_position_name():
    global position_name
    global currentPosNum
    if 0:
        while 1:
            randomPosition = random.sample(_position_name_list, len(_position_name_list))
            if position_name != randomPosition[0]:
                position_name = randomPosition[0]
                return position_name
            else:
                # print("start>")
                # print("0>" + str(randomPosition[0]))
                # print("1>"+ str(randomPosition[1]))
                position_name = randomPosition[1]
                print(position_name)
                # print("<end")
                return position_name
    else:
        position_name = _position_name_list[currentPosNum]
        print("currentPosNum>" + str(currentPosNum) + "listLength>" + str(len(_position_name_list)))
        currentPosNum += 1
        if currentPosNum >= len(_position_name_list):
            currentPosNum = 0
        print("currentPosNum>" + str(currentPosNum) + "listLength>" + str(len(_position_name_list)))
        return position_name


# 通过标定点名称获取坐标信息
def get_position_XYZ_by_name(positionName):
    return _position_name_dict[positionName]


def set_position_name_by_serial(serial_dict):
    _position_name_list.clear()
    _position_name_dict.clear()
    for key in serial_dict:
        _position_name_list.append(key)
        _position_name_dict[key] = serial_dict[key]


def set_value(key, value):
    global _global_dict
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
