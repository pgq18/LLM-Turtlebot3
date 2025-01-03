import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
import roslibpy
# /* 默认端口9090
# */
client = roslibpy.Ros(host='192.168.145.17', port=9090)
client.run()
talker = roslibpy.Topic(client, '/chatter', 'std_msgs/String')

cap = cv2.VideoCapture(0)

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the image mode:
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='./gesture_recognizer.task'),
    running_mode=VisionRunningMode.IMAGE)
print("fffff")
with GestureRecognizer.create_from_options(options) as recognizer:
    while cap.isOpened():
        if not cap.isOpened():
            print("camera not opened")
            break
        ret, frame = cap.read()
        if not ret:
            print("camera not opened")
            break
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        out = recognizer.recognize(mp_image)
        if len(out.gestures) != 0:
            if out.gestures[0][0].category_name != "None":
                if out.gestures[0][0].category_name == "Open_Palm":
                    talker.publish(roslibpy.Message({'data': 'self.forward(0.2)'}))
                    print("+++++++++ forward +++++++++")
                elif out.gestures[0][0].category_name == "Pointing_Up":
                    talker.publish(roslibpy.Message({'data': 'self.backward(0.2)'}))
                    print("+++++++++ backward +++++++++")
                elif out.gestures[0][0].category_name == "Closed_Fist":
                    talker.publish(roslibpy.Message({'data': 'self.left(45)'}))
                    print("+++++++++ left +++++++++")
                elif out.gestures[0][0].category_name == "Thumb_Up":
                    talker.publish(roslibpy.Message({'data': 'self.right(45)'}))
                    print("+++++++++ right +++++++++")
                print(out.gestures[0][0].category_name)
                time.sleep(2)
    talker.unadvertise()
    client.terminate()