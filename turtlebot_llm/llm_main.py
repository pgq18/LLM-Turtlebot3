from spark_lite import spark_lite
from iat_ws_python3 import iat

import keyboard
import requests
import json

import time
import roslibpy
# /* 默认端口9090
# */
client = roslibpy.Ros(host='192.168.145.17', port=9090)
client.run()
talker = roslibpy.Topic(client, '/chatter', 'std_msgs/String')

quit = False

def on_key(event):
    global quit
    if event.name == 'space':
        iat_result = iat()
        out = spark_lite(iat_result)
        p1 = out.split('```python')[1]
        p2 = p1.split('```')[0]
        talker.publish(roslibpy.Message({'data': p2}))
    if event.name == 'esc':
        talker.unadvertise()
        client.terminate()
        quit = True

def main():
    while True:
        keyboard.on_press(on_key)
        if quit:
            break
        keyboard.wait()

if __name__ == "__main__":
    main()

