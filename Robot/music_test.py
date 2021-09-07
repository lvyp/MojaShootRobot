import os
import queue
import threading
import time
import wave  # 导入音频处理包
# import matplotlib.pyplot as plt
import numpy as np
import globalVariable
from MoJaTimer import timerMachine
# from actionMode import expressionDict

#init degree
# 5#: 300.96  6#: 221.76 16#: 585 17#: 45
#15#: 285.12

#range degree
# 5#: 27.28↓  6#: 27.28↑
#15#: 37.84↓

TIME_RANGE = 0.05 #sec

START_DEGREE_5 = 300.96
START_DEGREE_6 = 221.76
START_DEGREE_15 = 285.12

CHILD_ROM = 27.28 #range of motion 27.28°
OLD_ROM = 37.84 #range of motion 37.84°

motor_dist = {"id": 1, "degree":5}
motor5_dist = {"id": 5, "degree":5}
motor6_dist = {"id": 6, "degree":5}
motor15_dist = {"id": 15, "degree":5}

queue_action_sound = queue.Queue(1)
#电机
# def mouth_motor(que2, que):
#     print("expressionDict threading",id(que))
#     while 1:
#         motor_obj = que2.get()
#
#         if "id" in motor_obj and "degree" in motor_obj:
#             # print(motor_obj["id"], motor_obj["degree"])
#             if motor_obj["id"] == 5:
#                 for var in expressionDict["talk_list"]:
#                     if var.get("id") == 5:
#                         var["degree"] = str(motor_obj["degree"])
#                     if var.get("id") == 6:
#                         var["degree"] = str(round(START_DEGREE_6 + (START_DEGREE_5 - motor_obj["degree"]), 2))
#             if motor_obj["id"] == 15:
#                 for var in expressionDict["talk_list"]:
#                     if var.get("id") == 15:
#                         var["degree"] = str(motor_obj["degree"])
#             # 表情
#             que.put(talk_arr)
            # 表情
            # globalVariable.m_express["expression"] = "old_talk_list"

# def mouth_parse(que):
#

#解析
def mouth_action(que):
    fistPlay = 0
    while 1:
        file_name = queue_action_sound.get() #queue_action_sound form play_test.py  queue_action_sound = Queue()
        print("mouth_action recv:", file_name)
        currentTime = timerMachine()
        # print("", file, currentTime, fistPlay)
        if os.path.isfile(file_name) == False and (currentTime - fistPlay < 5):
            print("file is no-exist")
            continue

        fistPlay = currentTime
        f = wave.open(file_name, 'rb')
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        # nchannels:声道数;sampwidth:量化位数（byte）;framerate:采样频率;nframes:采样点数
        print('channel:', 1, 'sampwidth:', sampwidth, 'framerate:', framerate, 'numframes:', nframes)
        strData = f.readframes(nframes)  # 读取音频，字符串格式
        f.close()
        # waveData = np.frombuffer(strData, dtype='S1', offset=0)
        waveData = np.frombuffer(strData, dtype=np.short)  # 将字符串转化为int

        waveData.shape = -1, 2  # 将waveData数组改为2列，行数自动匹配。

        waveData = waveData.T

        time_list = np.arange(0, nframes) * (1.0 / framerate)
        MOM = 2000
        print("max of motion", MOM)

        sleep_time = 0.0

        for i in range(0, nframes, int(TIME_RANGE * framerate)):
            if (waveData[0][i] > 0):
                time.sleep(time_list[i] - sleep_time)
                sleep_time = time_list[i]
                wave_data = float(waveData[0][i])
                if wave_data > MOM:
                    wave_data = MOM
                degree_child = CHILD_ROM / float(MOM) * wave_data
                # print("degree_child", round(degree_child, 2))
                # print("5#:, ", round(START_DEGREE_5 - degree_child, 2), "   6#:", round(START_DEGREE_6 + degree_child, 2), "   time:", round(time_list[i], 3))

                motor5_dist["degree"] = round(START_DEGREE_5 - degree_child, 2)
                que.put(motor5_dist)
                motor6_dist["degree"] = round(START_DEGREE_6 + degree_child, 2)
                que.put(motor6_dist)

                # motor6_dist["degree"] = round(START_DEGREE_6 - degree_child, 2)
                # que.put(motor6_dist)

            if (waveData[1][i] > 0):
                time.sleep(time_list[i] - sleep_time)
                sleep_time = time_list[i]
                wave_data = float(waveData[1][i])
                if wave_data > MOM:
                    wave_data = MOM
                degree_old = OLD_ROM / float(MOM) * float(wave_data)
                # print("degree_old", round(degree_old, 2))
                # print("15#:", round(START_DEGREE_15 - degree_old, 2), "   time:", round(time_list[i], 3))

                motor15_dist["degree"] = round(START_DEGREE_15 - degree_old, 2)
                que.put(motor15_dist)
        if queue_action_sound.empty() == False:
            file_name = queue_action_sound.get_nowait()
            print("queue_action_sound.get_nowait", file_name)
        # queue_action_sound.get_nowait()
        # queue_action_sound.get()
        # plt.figure(1)
        # plt.subplot(2, 1, 1)
        # plt.plot(time_list, waveData[0])
        #
        # plt.subplot(2, 1, 2)
        # plt.plot(time_list, waveData[1], c='r')
        # plt.xlabel("Time(s)")
        # plt.show()

def music_main(que):
    # play_main()
    # motor_init()
    # queue_motor = queue.Queue(maxsize = 1)

    # 创建线程
    thread_mouth = threading.Thread(target=mouth_action, args = (que, ))
    # thread_motor = threading.Thread(target=mouth_motor, args = (queue_motor, que))

    # 启动线程
    thread_mouth.start()
    # thread_motor.start()

if __name__ == '__main__':
    music_main()
