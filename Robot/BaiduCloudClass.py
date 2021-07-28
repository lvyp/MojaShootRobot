#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2021/6/11 10:12
# @Author :
# @Site : Beijing
# @File : BaiduCloudClass.py
# @Software: PyCharm
import json
import os

import pyaudio
import tqdm as tqdm
import requests
from aip import AipSpeech, AipNlp
from loggerMode import logger
import globalVariable as GV


class Baidu_NLU(object):
    def __init__(self):
        self.API_Key = "EI3cSUrazGNTbeCIU4R4IQ8e"
        self.Secret_Key = "ENbN0tsyS5QnlqeFznp6S5XltZfWkHLp"
        self.AppID = "S54880"
        self.access_token = self.get_access_token()
        self.session_id = GV.session_id
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        self.body = {
            "version": "2.0",
            # "skill_ids":"",技能ID列表。我们允许开发者指定调起哪些技能。这个列表是有序的——排在越前面的技能，优先级越高。技能优先级体现在response的排序上。
            "log_id": "UNITTEST_10000",  # 开发者需要在客户端生成的唯一id，用来定位请求，响应中会返回该字段。对话中每轮请求都需要一个log_id
            "session_id": self.session_id,
            # session保存机器人的历史会话信息，由机器人创建，客户端从上轮应答中取出并直接传递，不需要了解其内容。如果为空，则表示清空session（开发者判断用户意图已经切换且下一轮会话不需要继承上一轮会话中的词槽信息时可以把session置空，从而进行新一轮的会话）。session字段内容较多，开发者可以通过传送session_id的方式节约传输流量。
            "bot_id": "1099740",
            "skill_sessions": "",

            "service_id": self.AppID,  # 机器人ID，service_id 与skill_ids不能同时缺失，至少一个有值·
            "request": {"query": "", "user_id": "88888"},
            "dialog_state": {
                "contexts": {"SYS_REMEMBERED_SKILLS": ["1107705", "1099737", "1101887"]}
            }
        }

    def get_access_token(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(
            self.API_Key, self.Secret_Key)
        response = requests.get(host)
        return (response.json().get("access_token"))

    def get_NLU(self, text):
        url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + self.access_token

        self.body["request"]["query"] = text
        try:
            print("session_id_old:" + self.body["session_id"])
            response = requests.post(url=url, data=json.dumps(self.body), headers=self.headers)
            if response:
                json_result = response.json().get("result")
                print(json_result)
                GV.session_id = json_result.get("session_id")
                print("session_id_new:" + self.body["session_id"])
                answer = json_result.get("response_list")[0]
                return answer
        except Exception as e:
            logger.info("ASR Exception Happened: " + str(e))
            return {"error": "Exception Happened"}


class BaiduCloud(object):
    def __init__(self):
        self.Cloud_AppID = "24343144"
        self.Cloud_APIKey = "E1GPVi0geOh8ufvROWC7NOz2"
        self.Cloud_Secret_Key = "iCvIBWCrEG2E8OBfmIiVWU3dgGZPT9B9"
        self.AipSpeechclient = AipSpeech(self.Cloud_AppID, self.Cloud_APIKey, self.Cloud_Secret_Key)
        self.NLPclient = AipNlp(self.Cloud_AppID, self.Cloud_APIKey, self.Cloud_Secret_Key)

    def ASR(self):
        try:
            pa = pyaudio.PyAudio()
            stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                             frames_per_buffer=2048)
            record_buf = []
            print("开始ASR指令收集")
            pbar = tqdm.tqdm(range(100))
            for i in pbar:
                audio_data = stream.read(516)
                record_buf.append(audio_data)
            # 关闭占用的资源
            pbar.close()
            # 停止声卡
            stream.stop_stream()
            # 关闭声卡
            stream.close()
            # 终止pyaudio
            pa.terminate()

            asr_result = self.AipSpeechclient.asr("".encode().join(record_buf), "wav", 16000, {"dev_pid": 1537, }).get(
                "result")
            if asr_result is None:
                print("没有识别结果")
            else:
                return asr_result[0]
        except Exception as e:
            logger.info("ASR Exception Happened: " + str(e))
            return "Exception Happened"

    def call_asr(self, filePath):
        with open(filePath, "rb") as fp:
            try:
                asr_result = self.AipSpeechclient.asr(fp.read(), "wav", 16000, {
                    "dev_pid": 1537,
                })
                if asr_result["result"] == "":
                    return ""
                else:
                    return asr_result.get("result")[0]
            except Exception as e:
                logger.info("ASR Exception Happened: " + str(e))
                return "Exception Happened"

    def call_tts(self, text):
        try:
            result = self.AipSpeechclient.synthesis(text, "zh", 1, {
                "vol": 5,
            })
            if not isinstance(result, dict):
                if os.path.exists("./TtsRecording/BaiduCloud/TtsResponse.mp3"):
                    os.remove("./TtsRecording/BaiduCloud/TtsResponse.mp3")
                else:
                    pass
                with open("./TtsRecording/BaiduCloud/TtsResponse.mp3", "wb") as f:
                    f.write(result)
            return "Successful"
        except Exception as e:
            logger.info("NLU Exception Happened: " + str(e))
            return "Exception Happened"

