# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# import rclpy
# from rclpy.executors import ExternalShutdownException
# from rclpy.node import Node

# from std_msgs.msg import String


# class MinimalPublisher(Node):

#     def __init__(self):
#         super().__init__('minimal_publisher')
#         self.publisher_ = self.create_publisher(String, 'topic', 10)
#         timer_period = 0.5  # seconds
#         self.timer = self.create_timer(timer_period, self.timer_callback)
#         self.i = 0

#     def timer_callback(self):
#         msg = String()
#         msg.data = 'Hello World: %d' % self.i
#         self.publisher_.publish(msg)
#         self.get_logger().info('Publishing: "%s"' % msg.data)
#         self.i += 1

# def main(args=None):
#     rclpy.init(args=args)
#     minimal_publisher = MinimalPublisher()
#     rclpy.spin(minimal_publisher)
#     minimal_publisher.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()
# import rclpy
# from rclpy.node import Node
# from geometry_msgs.msg import Twist  # 导入Twist消息类型
# import time

# class TwistPublisher(Node):

#     def __init__(self):
#         super().__init__('twist_publisher')
#         self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)  # 发布到'cmd_vel'话题

#     def forward(self):
#         # """使小车前进1米"""
#         msg = Twist()
#         msg.linear.x = 0.5  # 设置线速度为0.5 m/s
#         msg.angular.z = 0.0
#         for i in range(10000):
#             self.publisher_.publish(msg)
#             time.sleep(0.1)
#         self.get_logger().info('Moving forward 1m')
#         time.sleep(2)  # 前进1米，假设速度为0.5 m/s，需要2秒
#         self.stop()

#     def backward(self):
#         # """使小车后退1米"""
#         msg = Twist()
#         msg.linear.x = -0.5  # 设置线速度为-0.5 m/s
#         msg.angular.z = 0.0
#         self.publisher_.publish(msg)
#         self.get_logger().info('Moving backward 1m')
#         time.sleep(2)  # 后退1米，假设速度为0.5 m/s，需要2秒
#         self.stop()

#     def left(self):
#         # """使小车左转90°"""
#         msg = Twist()
#         msg.linear.x = 0.0
#         msg.angular.z = 0.5  # 设置角速度为0.5 rad/s
#         self.publisher_.publish(msg)
#         self.get_logger().info('Turning left 90°')
#         time.sleep(3.14)  # 假设角速度为0.5 rad/s，转90°（π/2）需要3.14秒
#         self.stop()

#     def right(self):
#         # """使小车右转90°"""
#         msg = Twist()
#         msg.linear.x = 0.0
#         msg.angular.z = -0.5  # 设置角速度为-0.5 rad/s
#         self.publisher_.publish(msg)
#         self.get_logger().info('Turning right 90°')
#         time.sleep(3.14)  # 假设角速度为0.5 rad/s，转90°（π/2）需要3.14秒
#         self.stop()

#     def stop(self):
#         # """停止小车运动"""
#         msg = Twist()
#         msg.linear.x = 0.0
#         msg.angular.z = 0.0
#         self.publisher_.publish(msg)
#         self.get_logger().info('Stopping')

# def main(args=None):
#     rclpy.init(args=args)
#     twist_publisher = TwistPublisher()

#     try:
#         # 循环调用 forward 函数，测试是否正常运行
#         while rclpy.ok():
#             twist_publisher.forward()
#             time.sleep(1)  # 停顿1秒以避免连续调用影响观测效果

#     except KeyboardInterrupt:
#         twist_publisher.get_logger().info('Keyboard Interrupt (SIGINT)')
#     finally:
#         twist_publisher.stop()  # 确保退出时停止小车
#         twist_publisher.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()


import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist  # 导入Twist消息类型
from std_msgs.msg import String
import time

class TwistPublisher(Node):

    def __init__(self):
        super().__init__('twist_publisher')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)  # 发布到'cmd_vel'话题
        self.subscription = self.create_subscription(String,'chatter',self.listener_callback, 10)
        # timer_period = 3  # 每3秒发布一次
        # self.timer = self.create_timer(timer_period, self.timer_callback)

    def listener_callback(self, msg):
        exec(msg.data)
        self.get_logger().info('I heard: "%s"' % msg.data)

    # def timer_callback(self):
    #     # msg = Twist()
    #     # # 设置线速度和角速度
    #     # msg.linear.x = 0.5  # x方向线速度
    #     # msg.linear.y = 0.0
    #     # msg.linear.z = 0.0

    #     # msg.angular.x = 0.0
    #     # msg.angular.y = 0.0
    #     # msg.angular.z = 0.5  # z方向角速度

    #     # self.publisher_.publish(msg)  # 发布消息
    #     # self.get_logger().info('Publishing Twist: linear x=%.2f, angular z=%.2f' % (msg.linear.x, msg.angular.z))
    #     self.forward()

    def forward(self, d):
        # """使小车前进1米"""
        msg = Twist()
        msg.linear.x = 0.1  # 设置线速度为0.1 m/s
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        for i in range(int(752*d)):
            self.publisher_.publish(msg)
            time.sleep(0.01)
            self.get_logger().info("aaaaaaaa")
        self.get_logger().info('Moving forward {}m'.format(d))
        time.sleep(0.5)
        self.stop()

    def backward(self, d):
        # """使小车后退1米"""
        msg = Twist()
        msg.linear.x = -0.1  # 设置线速度为-0.1 m/s
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0
        for i in range(int(752*d)):
            self.publisher_.publish(msg)
            time.sleep(0.01)
            self.get_logger().info("bbbbbbbb")
        self.get_logger().info('Moving backward {}m'.format(d))
        time.sleep(0.5)
        self.stop()

    def left(self, d):
        # """使小车左转90°"""
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.5  # 设置角速度为0.5 rad/s
        for i in range(int(220*d/90)):
            self.publisher_.publish(msg)
            time.sleep(0.01)
            self.get_logger().info("ccccccccc")
        self.get_logger().info('Turning left {}°'.format(d))
        time.sleep(0.5)
        self.stop()

    def right(self, d):
        # """使小车右转90°"""
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = -0.5  # 设置角速度为-0.5 rad/s
        for i in range(int(220*d/90)):
            self.publisher_.publish(msg)
            time.sleep(0.01)
            self.get_logger().info("ddddddddddd")
        self.get_logger().info('Turning right {}°'.format(d))
        time.sleep(0.5)
        self.stop()

    def stop(self):
        # """停止小车运动"""
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Stopping')

def main(args=None):
    rclpy.init(args=args)
    twist_publisher = TwistPublisher()

    try:
        rclpy.spin(twist_publisher)  # 保持节点运行
    except KeyboardInterrupt:
        twist_publisher.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        twist_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()