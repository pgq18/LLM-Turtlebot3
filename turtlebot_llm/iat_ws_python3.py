# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下，您可自行逐一或者复制到一个新的txt文件利用pip一次性安装：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#
#  语音听写流式 WebAPI 接口调用示例 接口文档（必看）：https://doc.xfyun.cn/rest_api/语音听写（流式版）.html
#  webapi 听写服务参考帖子（必看）：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38947&extra=
#  语音听写流式WebAPI 服务，热词使用方式：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--个性化热词，
#  设置热词
#  注意：热词只能在识别的时候会增加热词的识别权重，需要注意的是增加相应词条的识别率，但并不是绝对的，具体效果以您测试为准。
#  语音听写流式WebAPI 服务，方言试用方法：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--识别语种列表
#  可添加语种或方言，添加后会显示该方言的参数值
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

import pyaudio

from spark_lite import spark_lite

recording_results=""   # 识别结果
STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

stop = False


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo":1,"vad_eos":10000}

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


# 收到websocket消息的处理
def on_message(ws, message):
    # try:
    #     code = json.loads(message)["code"]
    #     sid = json.loads(message)["sid"]
    #     if code != 0:
    #         errMsg = json.loads(message)["message"]
    #         print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

    #     else:
    #         data = json.loads(message)["data"]["result"]["ws"]
    #         # print(json.loads(message))
    #         result = ""
    #         for i in data:
    #             for w in i["cw"]:
    #                 result += w["w"]
    #         print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))
    # except Exception as e:
    #     print("receive msg,but parse exception:", e)


    # 收到websocket消息的正常处理
    global stop
    try:
        # print(json.loads(message))
        code = json.loads(message)["code"]
        # 解码返回的message的json数据中的code
        sid = json.loads(message)["sid"]
        if code != 0:
            errMsg = json.loads(message)["message"]
            # 解码message中错误信息
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:
            data = json.loads(message)["data"]["result"]["ws"]
            # 解码message中ws数据
            result = ""
            for i in data:
                for w in i["cw"]:
                    result += w["w"]

            if result == '。' or result == '.。' or result == ' .。' or result == ' 。':
                pass
            else:
                # t.insert(END, result)  # 把上边的标点插入到result的最后
                print("翻译结果: %s。" % (result))
                global recording_results
                recording_results=result
    except Exception as e:
        # 异常处理，参数异常
        print("receive msg,but parse exception:", e)
    stop = True

# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,a,b):
    print("### closed ###")


# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        # 在线音频处理并发送到讯飞
        status=STATUS_FIRST_FRAME
        # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧
        CHUNK = 520  # 定义数据流块
        FORMAT = pyaudio.paInt16  # 16bit编码格式
        CHANNELS = 1  # 单声道
        RATE = 16000  # 16000采样频率
        p=pyaudio.PyAudio()  # 录音
        # 实例化pyaudio对象
        stream = p.open(format=FORMAT,  # 音频流wav格式
                        channels=CHANNELS,  # 单声道
                        rate=RATE,  # 采样率16000
                        input=True,
                        frames_per_buffer=CHUNK)
        # 创建音频流，使用这个对象去打开声卡，设置采样深度、通道数、采样率、输入和采样点缓存数量
        print("---------------开始录音-----------------")
        # 开始录音
        global text, stop
        for i in range(0,int(RATE/CHUNK*60)):
            # 录制特定时间的音频
            buf=stream.read(CHUNK)
            # 读出声卡缓冲区的音频数据
            if not buf:
                status=STATUS_LAST_FRAME
            if status==STATUS_FIRST_FRAME:
                # 首帧处理
                d = {"common": wsParam.CommonArgs,
                     "business": wsParam.BusinessArgs,
                     "data": {"status": 0, "format": "audio/L16;rate=16000",
                              "audio": str(base64.b64encode(buf), 'utf-8'),
                              "encoding": "raw"}}
                d = json.dumps(d)
                # 将拼接的字符串d数据结构转换为json
                ws.send(d)
                status=STATUS_CONTINUE_FRAME
            elif status==STATUS_CONTINUE_FRAME:
                # 中间帧处理
                d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                              "audio": str(base64.b64encode(buf), 'utf-8'),
                              "encoding": "raw"}}
                ws.send(json.dumps(d))
            elif status==STATUS_LAST_FRAME:
                # 最后一帧处理
                d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                              "audio": str(base64.b64encode(buf), 'utf-8'),
                              "encoding": "raw"}}
                ws.send(json.dumps(d))
                time.sleep(1)
                break
            if stop:
                stop = False
                break
        ws.close()

    thread.start_new_thread(run, ())



wsParam = Ws_Param(APPID='', 
                   APISecret='', 
                   APIKey='',
                   AudioFile='./iat_pcm_16k.pcm')
websocket.enableTrace(False)
wsUrl = wsParam.create_url()
ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
def iat():
    time1 = datetime.now()
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    time2 = datetime.now()
    print(time2-time1)
    print(recording_results)
    return recording_results
    out = spark_lite(recording_results)
    p1 = out.split('```python')[1]
    p2 = p1.split('```')[0]

    print(p2)

import keyboard

def on_key(event):
    if event.name == 'space':
        iat()
        
        # spark_lite(recording_results)


if __name__ == "__main__":
    # # 测试时候在此处正确填写相关信息即可运行
    # time1 = datetime.now()
    # wsParam = Ws_Param(APPID='faabd546', APISecret='YjgwNWEwMTMzODZlNjc3OTgyZTg3ZGQx',
    #                    APIKey='3f4acc2a1043463f2edc4d6b5aae93c8',
    #                    AudioFile='./iat_pcm_16k.pcm')
    # websocket.enableTrace(False)
    # wsUrl = wsParam.create_url()
    # ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    # ws.on_open = on_open
    # ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    # time2 = datetime.now()
    # print(time2-time1)

    while True:
        keyboard.on_press(on_key)
        keyboard.wait()
        # iat()
    # keyboard.on_press(on_key)
    # keyboard.wait()