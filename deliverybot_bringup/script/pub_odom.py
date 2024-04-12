#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import PointCloud2

class OdometryPublisher(Node):
    def __init__(self):
        super().__init__('odometry_publisher')
        self.subscription = self.create_subscription(
            PointCloud2,
            '/livox/lidar_192_168_1_109',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(Odometry, 'odom', 10)
        # self.publish_odometry(0.0,0.0,0.0,0.0,0.0,0.0,0.0)
        print("hi")

    def publish_odometry(self, x, y, z, quat_x, quat_y, quat_z, quat_w):
        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = x
        msg.pose.pose.position.y = y
        msg.pose.pose.position.z = z
        msg.pose.pose.orientation.x = quat_x
        msg.pose.pose.orientation.y = quat_y
        msg.pose.pose.orientation.z = quat_z
        msg.pose.pose.orientation.w = quat_w
        self.publisher_.publish(msg)

    def listener_callback(self, msg):
        self.publish_odometry(0.0,0.0,0.0,0.0,0.0,0.0,0.0)



def main(args=None):
    rclpy.init(args=args)
    node = OdometryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
