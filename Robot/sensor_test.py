# test
import multiprocessing
import threading
import time

import pygame
import serial

import globalVariable
from playVideoByPyGame import queBgm, play_bgm
from sensorCountMode import SensorCount
# from motor_test import *
import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

tick_time = 1 / 1000 # 1ms

elimi_time = 2 # ms 读取时间间隔
interval_time = 200 # ms 触发时间间隔
sound = pygame.mixer.Sound("./tts/HuVideo_Wav/shootIn.wav")  # 播放
#事件同步
event = threading.Event()

# def test_thread():
#     while 1:
#         """线程运行函数"""
#         # 进行计数通信
#         scoreFlag = sensor.getPortVal()
#         if scoreFlag:
#             event.set()  # 计数器获得锁
#             time.sleep(elimi_time * tick_time)
#
# def sem_thread():
#     c = 0
#     while 1:
#         """线程运行函数"""
#         event.wait() #阻塞等待
#         c = c + 1
#         print("线程同步 ", c)
#         ModbusRTU_Master(c)
#         time.sleep(interval_time * tick_time)
#         event.clear()
#         print("线程清零")

def sensorCount():
    sensor = SensorCount()
    score = 0
    while 1:
        # 进行计数通信
        scoreFlag = sensor.getPortVal()
        # print("进行计数通信")
        if scoreFlag:
            score = score + 1
            # ModbusRTU_Master(score)
            print(str(score))
            # 播放打击音效
            # globalVariable.talk_1 = "./tts/HuVideo_Wav/shootIn.wav"
            sound.set_volume(1)  # 设置声音
            sound.play()  # 播放音乐
            # globalVariable.playFlag = True
            time.sleep(1)
        else:
            # time.sleep(0.002)
            pass

def main():
    if 1:
        # # 创建线程
        # thread_hi = threading.Thread(target=play_bgm)
        # # 启动线程
        # thread_hi.start()
        # 为传感器创建单独进程，防止资源被强占
        sensorProcess = multiprocessing.Process(target=sensorCount)
        sensorProcess.start()


# 数据接收端
# def ModbusRTU_Master(score):
#     try:
#         # 设定串口为从站
#         # 外置参数包括端口 port = "COM3" 波特率：9600
#         master = modbus_rtu.RtuMaster(serial.Serial(port="com7",baudrate=9600, bytesize=8, parity='N', stopbits=1))
#         master.set_timeout(1.0)
#         master.set_verbose(True)
#         # 读保持寄存器
#         master.execute(slave=1, function_code=cst.WRITE_MULTIPLE_REGISTERS,
#                                 starting_address=20012, quantity_of_x=2, output_value=[score, 0])
#     except Exception as exc:
#         print(str(exc))

if __name__ == '__main__':
    globalVariable._init()
    # motor_init()
    # ModbusRTU_Master(0)
    # sensor = SensorCount()
    main()