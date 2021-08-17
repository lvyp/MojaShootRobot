# -*- coding: utf-8 -*-
# @Time : 2021/8/9 10:47
# @Author :
# @Site : Beijing
# @File : actionMode.py
# @Software: PyCharm
import time

from canMotor import CanMotor
from comMotor import ComMotor
TIMEOUT = 0.01

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
        {"id": 12, "degree": "227.04"},
        {"id": 13, "degree": "305.8"},
        {"id": 14, "degree": "94.16"},
        {"id": 15, "degree": "285.12"},
        {"id": 16, "degree": "54"},
        {"id": 17, "degree": "-54"},
        {"id": 18, "degree": "0"}
    ],
    "happy":
    [
        {"id": 1, "degree": "143.44"},
        {"id": 2, "degree": "208.56"},
        {"id": 3, "degree": "311.96"},
        {"id": 4, "degree": "277.2"},
        {"id": 5, "degree": "273.68"},
        {"id": 6, "degree": "249.04"},
        {"id": 7, "degree": "64.68"},
        {"id": 8, "degree": "156.64"},
        {"id": 9, "degree": "137.28"},
        {"id": 10, "degree": "209.88"},
        {"id": 11, "degree": "50.16"},
        {"id": 12, "degree": "227.04"},
        {"id": 13, "degree": "305.8"},
        {"id": 14, "degree": "161.92"},
        {"id": 15, "degree": "285.12"},
        {"id": 16, "degree": "-352.8"},
        {"id": 17, "degree": "352.8"},
        {"id": 18, "degree": "0"}
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
        {"id": 16, "degree": "54"},
        {"id": 17, "degree": "-54"},
        {"id": 18, "degree": "0"}
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
        {"id": 16, "degree": "54"},
        {"id": 17, "degree": "-54"},
        {"id": 18, "degree": "0"}
    ]
}


def action(comMotor, canMotor, expression):

    infoList = expressionDict[expression]
    infoList = list(reversed(infoList))
    for info in infoList:
        if info['id'] < 16:
            comMotor.action(SCS_ID=info['id'], degree=info['degree'])
        else:
            canMotor.MOTOR_Ctr(MOTOR_ADDR=info['id'], POS=info['degree'])
        time.sleep(TIMEOUT)


def beard():
    comMotor.action(15, "247.28")
    time.sleep(1)
    comMotor.action(15, "285.12")
    time.sleep(1)


if __name__ == "__main__":
    comMotor = ComMotor("COM1")
    canMotor = CanMotor()
    canMotor.RUN_CAN()
    canMotor.MOTOR_INIT(16)
    canMotor.MOTOR_INIT(17)
    canMotor.MOTOR_INIT(18)
    while True:
        action(comMotor, canMotor, "init")
        time.sleep(3)
        # beard()
        action(comMotor, canMotor, "happy")
        time.sleep(3)
        # beard()
        action(comMotor, canMotor, "embarrassed")
        time.sleep(3)
        # beard()
        action(comMotor, canMotor, "anger")
        time.sleep(3)
        # beard()
