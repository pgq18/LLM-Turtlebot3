# LLM-Turtlebot3
Control TurtleBot3 with LLM and hand gestures. 

# Install
## Setup ROS2 Package
Follow the instruction in [TurtleBot3 - ROBOTIS e-Manual](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/) to setup the TurtleBot3 and the ROS2 environment on PC.

If you have not created workspace for your ROS2, please creaste one first, following the instruction in [ROS2: Creating a workspace](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html). And then create a new package in your workspace.
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
## Create environment
We recommend using conda to manage dependencies. Make sure to install [Conda](https://docs.anaconda.com/miniconda/) before proceeding. The code works well with `python 3.9` and the packages listed in [`requirements.txt`](./requirements.txt). It should be compatible with `python >= 3.9` for mediapipe requires `python 3.9-3.12`. 
```bash
conda create -n llm-turtlebot3 python=3.9
conda activate llm-turtlebot3
pip install -r requirements.txt
```

# Usage
On Turtlebot3, run the following command to bring up basic packages to start TurtleBot3 applications.
```bash
export TURTLEBOT3_MODEL=${TB3_MODEL}
ros2 launch turtlebot3_bringup robot.launch.py
```
Start TwistPublisher node on PC.
```bash
cd ~/ros2_ws
source install/setup.bash
ros2 run llm-turtlebot3 controler
```
## LLM Control

## Hand Gesture Control

# Examples

# Authors
[@pgq18](https://github.com/pgq18) (maintainer)  
[@FengDK666](https://github.com/FengDK666)
