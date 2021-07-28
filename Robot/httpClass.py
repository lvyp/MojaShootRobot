# -*- coding: utf-8 -*-
# @Time : 2021/6/24 09:37
# @Author :
# @Site : Beijing
# @File : httpClass.py
# @Software: PyCharm
import json

import requests
from loggerMode import logger


class HttpClass(object):
    def __init__(self):
        self.ip = "192.168.1.110"
        self.post_x = ""
        self.post_y = ""
        self.post_theta = ""
        self.post_x, self.post_y, self.post_theta = self.get_pose()
        self.target_list = self.get_target_list()

    def get_map(self):  # 获取地图
        url = "/reeman/map"
        recv = requests.get("http://" + self.ip + url)

    def get_pose(self):  # 获取机器人位置
        url = "/reeman/pose"
        recv = requests.get("http://" + self.ip + url)
        pose = eval(recv.text)
        return [pose.get("x"), pose.get("y"), pose.get("theta")]

    def get_target_list(self):  # 获取目标点列表
        url = "http://" + self.ip + "/reeman/android_target"
        target_list = requests.get(url).text
        return eval(target_list)

    def move_target(self, target):
        url = "http://" + self.ip + "/cmd/nav"
        if self.target_list.get(target):
            body = {"x": float(self.target_list.get(target)[0]), "y": float(self.target_list.get(target)[1]),
                    "theta": float(self.target_list.get(target)[2])}
            try:
                recv = requests.post(url=url, data=json.dumps(body))
                logger.info('=== status_code === ' + str(recv.status_code))  # 响应码
                if recv.ok:
                    return 1
                else:
                    return 0
            except Exception as e:
                logger.info('Http Post 请求超时，网络出现故障！!!')
        else:
            return 0

    def move_point(self, data):
        url = "cmd/nav_point"
        body = data
        recv = requests.post(url="http://" + self.ip + url, data=json.dumps(body))
        print(recv)

    def navi_route(self, route):
        url = "http://" + self.ip + "cmd/navi_route"
        body = {"name": "".format(route if route else "路线1")}
        recv = requests.post(url=url, data=json.dumps(body))
        print(recv)

    def save_routes(self, data: dict):
        url = "http://" + self.ip + "cmd/save_routes"
        # data = {"路线1":[
        # [-2.372309309534959,-0.6168487691742568],
        # [-2.965386636918698,-0.20427323708122036],
        # [-4.564116823779212,-0.20427323708122036],
        # [-4.744618619069918,0.20830229501181607],
        # [-1.727660040639588,-0.3332030908602943],
        # [-1.90816183593029,-1.2099260965579965]]}
        body = data
        recv = requests.post(url=url, data=json.dumps(body))


