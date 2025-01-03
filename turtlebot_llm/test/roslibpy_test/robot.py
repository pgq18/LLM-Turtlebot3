# import os
# from flask import Flask, request, jsonify
# import requests
# import json

# app = Flask(__name__)

# @app.route('/move', methods = ['POST'])
# def move():
#     print(request)
#     data_in = request.json
#     exec(data_in)
#     print(data_in)
#     return jsonify({'text' : data_in}) , 200

# if __name__ == "__main__":
#     app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80)))

import time
import roslibpy

# /* 默认端口9090
# */
client = roslibpy.Ros(host='192.168.145.17', port=9090)
client.run()

talker = roslibpy.Topic(client, '/chatter', 'std_msgs/String')

while client.is_connected:
    talker.publish(roslibpy.Message({'data': 'Hello World!'}))
    print('Sending message...')
    time.sleep(1)

talker.unadvertise()

client.terminate()