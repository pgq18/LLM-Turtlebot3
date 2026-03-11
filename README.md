# LLM-Turtlebot3

Control TurtleBot3 with LLM and hand gestures. Use voice commands powered by iFlytek Spark LLM or hand gestures recognized by MediaPipe to control your robot.

## Features

- **LLM Voice Control**: Convert natural language voice commands to robot control code using iFlytek Spark LLM
- **Hand Gesture Control**: Control the robot with hand gestures recognized by MediaPipe
- **ROS2 Integration**: Seamless integration with ROS2 ecosystem via rosbridge

## Project Structure

```
LLM-Turtlebot3/
├── turtlebot_control.py      # ROS2 node for receiving commands and controlling robot
├── turtlebot_llm/
│   ├── llm_main.py           # Main script for LLM voice control
│   ├── spark_lite.py         # iFlytek Spark LLM integration
│   └── iat_ws_python3.py     # iFlytek speech recognition (IAT)
├── hand/
│   └── hand_main.py          # Hand gesture control script
└── requirements.txt          # Python dependencies
```

## Install

### Setup ROS2 Package

Follow the instruction in [TurtleBot3 - ROBOTIS e-Manual](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/) to setup the TurtleBot3 and the ROS2 environment on PC.

If you have not created workspace for your ROS2, please create one first, following the instruction in [ROS2: Creating a workspace](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html). And then create a new package in your workspace.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
ros2 pkg create llm-turtlebot3 --build-type ament_python --dependencies rclpy std_msgs
```

Copy [`turtlebot_control.py`](./turtlebot_control.py) in this repository to the package directory.

```bash
cp [path_of_this_repo]/turtlebot_control.py ~/ros2_ws/src/llm-turtlebot3/llm-turtlebot3/
```

Edit `setup.py` in the package. Add the following line to the entry_points.

```python
# in ~/ros2_ws/src/llm-turtlebot3/llm-turtlebot3/setup.py
entry_points={
    'console_scripts': [
        'controler = llm-turtlebot3.turtlebot_control:main', # add this line
    ],
},
```

Build the package.

```bash
cd ~/ros2_ws
colcon build --packages-select llm-turtlebot3
```

### Create Environment

We recommend using conda to manage dependencies. Make sure to install [Conda](https://docs.anaconda.com/miniconda/) before proceeding. The code works well with `python 3.9` and the packages listed in [`requirements.txt`](./requirements.txt). It should be compatible with `python >= 3.9` for mediapipe requires `python 3.9-3.12`.

```bash
conda create -n llm-turtlebot3 python=3.9
conda activate llm-turtlebot3
pip install -r requirements.txt
```

### Configure API Keys

Before using LLM voice control, you need to configure your iFlytek API credentials:

1. Register at [iFlytek Open Platform](https://www.xfyun.cn/)
2. Create an application and get your API credentials
3. Edit `turtlebot_llm/spark_lite.py` and fill in your credentials:

```python
SPARKAI_APP_ID = 'your_app_id'
SPARKAI_API_SECRET = 'your_api_secret'
SPARKAI_API_KEY = 'your_api_key'
```

4. Edit `turtlebot_llm/iat_ws_python3.py` and fill in your credentials:

```python
wsParam = Ws_Param(APPID='your_app_id',
                   APISecret='your_api_secret',
                   APIKey='your_api_key',
                   AudioFile='./iat_pcm_16k.pcm')
```

## Usage

### Start TurtleBot3

On Turtlebot3, run the following command to bring up basic packages to start TurtleBot3 applications.

```bash
export TURTLEBOT3_MODEL=${TB3_MODEL}
ros2 launch turtlebot3_bringup robot.launch.py
```

### Start Control Server

On PC, start the TwistPublisher node and rosbridge server:

```bash
# Terminal 1: Start rosbridge server
ros2 launch rosbridge_server rosbridge_websocket_launch.xml

# Terminal 2: Start controller node
cd ~/ros2_ws
source install/setup.bash
ros2 run llm-turtlebot3 controler
```

### LLM Voice Control

Run the LLM control script:

```bash
cd /path/to/LLM-Turtlebot3
conda activate llm-turtlebot3
python turtlebot_llm/llm_main.py
```

**Controls:**
- Press `Space` to start voice recording, speak your command, then release
- Press `Esc` to exit

**Example voice commands:**
- "前进1米" (Move forward 1 meter)
- "左转90度，然后前进2米" (Turn left 90 degrees, then move forward 2 meters)
- "走一个边长为1米的正方形" (Walk a square with side length 1 meter)

### Hand Gesture Control

Download the MediaPipe gesture recognizer model from [MediaPipe](https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer) and place `gesture_recognizer.task` in the `hand/` directory.

Run the hand gesture control script:

```bash
cd /path/to/LLM-Turtlebot3/hand
conda activate llm-turtlebot3
python hand_main.py
```

**Gesture mappings:**
| Gesture | Action |
|---------|--------|
| Open Palm | Forward 0.2m |
| Pointing Up | Backward 0.2m |
| Closed Fist | Turn Left 45° |
| Thumb Up | Turn Right 45° |

**Note:** You may need to modify the IP address in `hand_main.py` and `llm_main.py` to match your robot's IP:

```python
client = roslibpy.Ros(host='YOUR_ROBOT_IP', port=9090)
```

## Available Robot Commands

The following commands can be used in generated code:

| Command | Description |
|---------|-------------|
| `self.forward(x)` | Move forward x meters |
| `self.backward(x)` | Move backward x meters |
| `self.left(x)` | Turn left x degrees |
| `self.right(x)` | Turn right x degrees |
| `self.stop()` | Stop the robot |

## Dependencies

- ROS2 Humble
- Python 3.9+
- MediaPipe
- OpenCV
- iFlytek SparkAI
- roslibpy
- PyAudio
- keyboard

## Authors

[@pgq18](https://github.com/pgq18) (maintainer)
[@FengDK666](https://github.com/FengDK666)

## License

This project is licensed under the MIT License.
