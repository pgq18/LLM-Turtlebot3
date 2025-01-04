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
    #     pass

    def forward(self, d):
        # """使小车前进"""
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
        self.get_logger().info('Moving forward {}m'.format(d))
        time.sleep(0.5)
        self.stop()

    def backward(self, d):
        # """使小车后退"""
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
        self.get_logger().info('Moving backward {}m'.format(d))
        time.sleep(0.5)
        self.stop()

    def left(self, d):
        # """使小车左转"""
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
        self.get_logger().info('Turning left {}°'.format(d))
        time.sleep(0.5)
        self.stop()

    def right(self, d):
        # """使小车右转"""
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