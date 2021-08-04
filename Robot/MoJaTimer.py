# -*- coding: utf-8 -*-
# @Time : 2021/8/3 14:30
# @Author :
# @Site : Beijing
# @File : MoJaTimer.py
# @Software: PyCharm
import datetime


def minChangeToSec(h, m, s):
    s = h * 60 * 60 + m * 60 + s
    return s


def timerMachine(startTime=0.000):
    dt_hms = datetime.datetime.now().strftime('%H:%M:%S.%f')
    h, m, s = dt_hms.strip().split(":")
    hms = minChangeToSec(float(h), float(m), float(s))
    # print("m: " + m + " s: " + s + " ms: " + str(ms) + " startTime: " + str(startTime))
    return float('%.3f' % (hms - startTime))