#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped


class ACDPlanner(Node):

    def __init__(self):
        super().__init__('acd_planner_node')
        self.get_logger().info("Adaptive Cell Decomposition Planner started")

        self.path_pub = self.create_publisher(Path, '/acd_path', 10)

        # Dummy path just to test node works
        self.publish_dummy_path()

    def publish_dummy_path(self):
        path = Path()
        path.header.frame_id = 'map'

        points = [(0.0, 0.0), (1.0, 0.0), (1.5, 1.0), (2.0, 2.0)]

        for x, y in points:
            pose = PoseStamped()
            pose.pose.position.x = x
            pose.pose.position.y = y
            path.poses.append(pose)

        self.path_pub.publish(path)
        self.get_logger().info("Dummy path published")


def main(args=None):
    rclpy.init(args=args)
    node = ACDPlanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

