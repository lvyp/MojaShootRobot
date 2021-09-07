# -*- coding: utf-8 -*-
# @Time : 2021/8/9 10:47
# @Author :
# @Site : Beijing
# @File : actionMode.py
# @Software: PyCharm
import queue
import random
import threading
import time
from canMotor import CanMotor
from comMotor import ComMotor
TIMEOUT = 0.05

expressionDict = {
    "init":
    [
        {"id": 1, "degree": "201.08"},
        {"id": 2, "degree": "208.56"},
        {"id": 3, "degree": "311.96"},
        {"id": 4, "degree": "217.8"},
        {"id": 5, "degree": "273.68"},
        {"id": 6, "degree": "249.04"},
        {"id": 7, "degree": "64.68"},
        {"id": 8, "degree": "195.36"},
        {"id": 9, "degree": "83.6"},
        {"id": 10, "degree": "209.88"},
        {"id": 11, "degree": "93.7"},
        {"id": 12, "degree": "245.96"},
        {"id": 13, "degree": "286.22"},
        {"id": 14, "degree": "94.16"},
        {"id": 15, "degree": "285.12"},
        {"id": 16, "degree": "684"},
        {"id": 17, "degree": "-54"}
    ],
    "happy":
    [
        {"id": 1, "degree": "143.44"},
        {"id": 2, "degree": "208.56"},
        {"id": 3, "degree": "311.96"},
        {"id": 4, "degree": "277.2"},
        {"id": 5, "degree": "273.68"},  # 嘴巴旋转
        {"id": 6, "degree": "249.04"},  # 嘴巴旋转
        {"id": 7, "degree": "64.68"},
        {"id": 8, "degree": "156.64"},
        {"id": 9, "degree": "137.28"},
        {"id": 10, "degree": "209.88"},
        {"id": 11, "degree": "50.16"},
        {"id": 12, "degree": "227.04"},
        {"id": 13, "degree": "305.8"},
        {"id": 14, "degree": "161.92"},
        {"id": 15, "degree": "285.12"},
        {"id": 16, "degree": "288"},     # 嘴巴上下
        {"id": 17, "degree": "342"}      # 嘴巴上下
    ],
    "embarrassed":
    [
        {"id": 1, "degree": "258.72"},
        {"id": 2, "degree": "169.84"},
        {"id": 3, "degree": "343.2"},
        {"id": 4, "degree": "158.4"},
        {"id": 5, "degree": "328.24"},
        {"id": 6, "degree": "194.48"},
        {"id": 7, "degree": "74.8"},
        {"id": 8, "degree": "234.08"},
        {"id": 9, "degree": "29.92"},
        {"id": 10, "degree": "199.76"},
        {"id": 11, "degree": "187.44"},
        {"id": 12, "degree": "189.2"},
        {"id": 13, "degree": "344.96"},
        {"id": 14, "degree": "26.4"},
        {"id": 15, "degree": "285.12"},
        {"id": 16, "degree": "684"},
        {"id": 17, "degree": "-54"}
    ],
    "anger":
    [
        {"id": 1, "degree": "258.72"},
        {"id": 2, "degree": "247.28"},
        {"id": 3, "degree": "280.72"},
        {"id": 4, "degree": "158.4"},
        {"id": 5, "degree": "273.68"},
        {"id": 6, "degree": "249.04"},
        {"id": 7, "degree": "54.56"},
        {"id": 8, "degree": "234.08"},
        {"id": 9, "degree": "29.92"},
        {"id": 10, "degree": "220"},
        {"id": 11, "degree": "187.44"},
        {"id": 12, "degree": "264.88"},
        {"id": 13, "degree": "266.64"},
        {"id": 14, "degree": "26.4"},
        {"id": 15, "degree": "285.12"},
        {"id": 16, "degree": "684"},
        {"id": 17, "degree": "-54"}
    ],
    "amazing":
    [
        {"id": 1, "degree": "143.44"},
        {"id": 2, "degree": "169.84"},
        {"id": 3, "degree": "343.2"},
        {"id": 4, "degree": "143.44"},
        {"id": 5, "degree": "273.68"},
        {"id": 6, "degree": "249.04"},
        {"id": 7, "degree": "54.56"},
        {"id": 8, "degree": "195.36"},
        {"id": 9, "degree": "83.6"},
        {"id": 10, "degree": "194.92"},
        {"id": 11, "degree": "50.16"},
        {"id": 12, "degree": "189.2"},
        {"id": 13, "degree": "344.96"},
        {"id": 14, "degree": "161.92"},
        {"id": 15, "degree": "247.28"},
        {"id": 16, "degree": "684"},
        {"id": 17, "degree": "-54"}
    ],
    "provoke":
    [
        {"id": 1, "degree": "258.72"},
        {"id": 2, "degree": "208.56"},
        {"id": 3, "degree": "311.96"},
        {"id": 4, "degree": "158.4"},
        {"id": 5, "degree": "273.68"},
        {"id": 6, "degree": "221.76"},
        {"id": 7, "degree": "54.56"},
        {"id": 8, "degree": "195.36"},
        {"id": 9, "degree": "83.6"},
        {"id": 10, "degree": "220"},
        {"id": 11, "degree": "187.44"},
        {"id": 12, "degree": "264.88"},
        {"id": 13, "degree": "266.64"},
        {"id": 14, "degree": "26.4"},
        {"id": 15, "degree": "285.12"},
        {"id": 16, "degree": "684"},
        {"id": 17, "degree": "342"}
    ],
    "init_speaking":
    [
        {"id": 1, "degree": "201.08"},
        {"id": 2, "degree": "208.56"},
        {"id": 3, "degree": "311.96"},
        {"id": 4, "degree": "217.8"},
        # {"id": 5, "degree": "273.68"},
        # {"id": 6, "degree": "249.04"},
        {"id": 7, "degree": "64.68"},
        {"id": 8, "degree": "195.36"},
        {"id": 9, "degree": "83.6"},
        {"id": 10, "degree": "209.88"},
        {"id": 11, "degree": "93.7"},
        {"id": 12, "degree": "245.96"},
        {"id": 13, "degree": "286.22"},
        {"id": 14, "degree": "94.16"},
        {"id": 15, "degree": "285.12"},
        # {"id": 16, "degree": "684"},
        # {"id": 17, "degree": "-54"}
    ],
    "happy_speaking":
    [
        {"id": 1, "degree": "143.44"},
        {"id": 2, "degree": "208.56"},
        {"id": 3, "degree": "311.96"},
        {"id": 4, "degree": "277.2"},
        # {"id": 5, "degree": "273.68"},  # 嘴巴旋转
        # {"id": 6, "degree": "249.04"},  # 嘴巴旋转
        {"id": 7, "degree": "64.68"},
        {"id": 8, "degree": "156.64"},
        {"id": 9, "degree": "137.28"},
        {"id": 10, "degree": "209.88"},
        {"id": 11, "degree": "50.16"},
        {"id": 12, "degree": "227.04"},
        {"id": 13, "degree": "305.8"},
        {"id": 14, "degree": "161.92"},
        {"id": 15, "degree": "285.12"},
        # {"id": 16, "degree": "288"},     # 嘴巴上下
        # {"id": 17, "degree": "342"}      # 嘴巴上下
    ],
    "embarrassed_speaking":
    [
        {"id": 1, "degree": "258.72"},
        {"id": 2, "degree": "169.84"},
        {"id": 3, "degree": "343.2"},
        {"id": 4, "degree": "158.4"},
        # {"id": 5, "degree": "328.24"},
        # {"id": 6, "degree": "194.48"},
        {"id": 7, "degree": "74.8"},
        {"id": 8, "degree": "234.08"},
        {"id": 9, "degree": "29.92"},
        {"id": 10, "degree": "199.76"},
        {"id": 11, "degree": "187.44"},
        {"id": 12, "degree": "189.2"},
        {"id": 13, "degree": "344.96"},
        {"id": 14, "degree": "26.4"},
        {"id": 15, "degree": "285.12"},
        # {"id": 16, "degree": "684"},
        # {"id": 17, "degree": "-54"}
    ],
    "anger_speaking":
    [
        {"id": 1, "degree": "258.72"},
        {"id": 2, "degree": "247.28"},
        {"id": 3, "degree": "280.72"},
        {"id": 4, "degree": "158.4"},
        # {"id": 5, "degree": "273.68"},
        # {"id": 6, "degree": "249.04"},
        {"id": 7, "degree": "54.56"},
        {"id": 8, "degree": "234.08"},
        {"id": 9, "degree": "29.92"},
        {"id": 10, "degree": "220"},
        {"id": 11, "degree": "187.44"},
        {"id": 12, "degree": "264.88"},
        {"id": 13, "degree": "266.64"},
        {"id": 14, "degree": "26.4"},
        {"id": 15, "degree": "285.12"},
        # {"id": 16, "degree": "684"},
        # {"id": 17, "degree": "-54"}
    ],
    "amazing_speaking":
    [
        {"id": 1, "degree": "143.44"},
        {"id": 2, "degree": "169.84"},
        {"id": 3, "degree": "343.2"},
        {"id": 4, "degree": "143.44"},
        # {"id": 5, "degree": "273.68"},
        # {"id": 6, "degree": "249.04"},
        {"id": 7, "degree": "54.56"},
        {"id": 8, "degree": "195.36"},
        {"id": 9, "degree": "83.6"},
        {"id": 10, "degree": "194.92"},
        {"id": 11, "degree": "50.16"},
        {"id": 12, "degree": "189.2"},
        {"id": 13, "degree": "344.96"},
        {"id": 14, "degree": "161.92"},
        {"id": 15, "degree": "247.28"},
        # {"id": 16, "degree": "684"},
        # {"id": 17, "degree": "-54"}
    ],
    "provoke_speaking":
    [
        {"id": 1, "degree": "258.72"},
        {"id": 2, "degree": "208.56"},
        {"id": 3, "degree": "311.96"},
        {"id": 4, "degree": "158.4"},
        # {"id": 5, "degree": "273.68"},
        # {"id": 6, "degree": "221.76"},
        {"id": 7, "degree": "54.56"},
        {"id": 8, "degree": "195.36"},
        {"id": 9, "degree": "83.6"},
        {"id": 10, "degree": "220"},
        {"id": 11, "degree": "187.44"},
        {"id": 12, "degree": "264.88"},
        {"id": 13, "degree": "266.64"},
        {"id": 14, "degree": "26.4"},
        {"id": 15, "degree": "285.12"},
        # {"id": 16, "degree": "684"},
        # {"id": 17, "degree": "342"}
    ]
}

emotion_arr = ["init", "happy", "embarrassed", "anger", "amazing", "provoke",
               "init_speaking", "happy_speaking", "embarrassed_speaking",
               "anger_speaking", "amazing_speaking", "provoke_speaking"]

def action(comMotor, canMotor, expression):
    infoList = expressionDict[expression]
    infoList = list(reversed(infoList))
    for info in infoList:
        if info['id'] < 16:
            comMotor.action(SCS_ID=info['id'], degree=info['degree'])
        else:
            canMotor.MOTOR_Ctr(MOTOR_ADDR=info['id'], POS=info['degree'])
        # time.sleep(TIMEOUT)

que_emotion = queue.Queue(18)
que1 = queue.Queue()
que2 = queue.Queue()
def emo_thread(que_in, que_out):
    while 1:
        emo = que_in.get()
        if emo in expressionDict:

                for arr in expressionDict[emo]:
                    emotion_dist = {"id": 1, "degree": 1}
                    emotion_dist["id"] = arr["id"]
                    emotion_dist["degree"] = float(arr["degree"])
                    # print(emotion_dist)
                    que_out.put(emotion_dist)

                time.sleep(1)

                for arr in expressionDict["init"]:
                    emotion_dist = {"id": 1, "degree": 1}
                    emotion_dist["id"] = arr["id"]
                    emotion_dist["degree"] = float(arr["degree"])
                    # print(emotion_dist)
                    que_out.put(emotion_dist)

                time.sleep(1)

                # for arr in expressionDict[emo]:
                #     emotion_dist = {"id": 1, "degree": 1}
                #     emotion_dist["id"] = arr["id"]
                #     emotion_dist["degree"] = float(arr["degree"])
                #     # print(emotion_dist)
                #     que_out.put(emotion_dist)
                #
                # time.sleep(1)
                #
                # for arr in expressionDict["init"]:
                #     emotion_dist = {"id": 1, "degree": 1}
                #     emotion_dist["id"] = arr["id"]
                #     emotion_dist["degree"] = float(arr["degree"])
                #     # print(emotion_dist)
                #     que_out.put(emotion_dist)




def action_process(que):
    comMotor = ComMotor("COM1")
    canMotor = CanMotor()
    canMotor.RUN_CAN()
    canMotor.MOTOR_INIT(16)
    canMotor.MOTOR_INIT(17)
    canMotor.MOTOR_INIT(18)
    canMotor.MOTOR_Ctr(MOTOR_ADDR=18, POS=0.0)
    while 1:
        motor_obj = que.get()

        #{id:"5", degree:123}
        if "id" in motor_obj and "degree" in motor_obj:
            # print("action_process que recv: id", motor_obj['id'], " degree", motor_obj['degree'])
            if motor_obj['id'] < 16:
                comMotor.action(SCS_ID=motor_obj['id'], degree=motor_obj['degree'])
            else:
                canMotor.MOTOR_Ctr(MOTOR_ADDR=motor_obj['id'], POS=motor_obj['degree'])
        # if str == "angle":
        #     canMotor.MOTOR_Ctr(MOTOR_ADDR=18, POS=expression["angle"])
        # else:
        #     infoList = expressionDict[str]
        #     infoList = list(reversed(infoList))
        #     for info in infoList:
        #         print("id = ", info['id'], "degree = ", info['degree'])
        #         if info['id'] < 16:
        #             comMotor.action(SCS_ID=info['id'], degree=info['degree'])
        #         else:
        #             canMotor.MOTOR_Ctr(MOTOR_ADDR=info['id'], POS=info['degree'])
        # if expression["expression"] != "none":
        #     infoList = expressionDict[expression["expression"]]
        #     infoList = list(reversed(infoList))
        #     for info in infoList:
        #         print("id = ", info['id'], "degree = ", info['degree'])
        #         if info['id'] < 16:
        #             comMotor.action(SCS_ID=info['id'], degree=info['degree'])
        #         else:
        #             canMotor.MOTOR_Ctr(MOTOR_ADDR=info['id'], POS=info['degree'])
        #         # time.sleep(TIMEOUT)
        #     expression["expression"] = "none"
        # else:
        #     pass
        # print(expression["expression"])
        # if "angle" in expression:
        #     canMotor.MOTOR_Ctr(MOTOR_ADDR=18, POS=expression["angle"])

# from music_test import mouth_action,mouth_motor

if __name__ == "__main__":
    emo = threading.Thread(target=emo_thread, args=(que1, que2))
    emo.start()
    emo1 = threading.Thread(target=action_process, args=(que2, ))
    emo1.start()

    for i in range(0, 6):

        que1.put(emotion_arr[i])
        print("que put times", i)
        time.sleep(5)
