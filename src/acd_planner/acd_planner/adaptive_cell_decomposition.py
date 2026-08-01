#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from nav_msgs.msg import OccupancyGrid
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point

import numpy as np


class AdaptiveCellDecomposition(Node):
    def __init__(self):
        super().__init__('adaptive_cell_decomposition')

        # Parameters
        self.base_cell_size = 20   # cells (coarse)
        self.min_cell_size = 5     # adaptive limit

        # Subscribers
        self.map_sub = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.map_callback,
            10
        )

        # Publishers
        self.marker_pub = self.create_publisher(
            MarkerArray,
            '/decomposition_cells',
            10
        )

        self.get_logger().info("Adaptive Cell Decomposition Node Started")

    def map_callback(self, msg):
        width = msg.info.width
        height = msg.info.height
        resolution = msg.info.resolution
        data = np.array(msg.data).reshape((height, width))

        marker_array = MarkerArray()
        marker_id = 0

        # Step 1: coarse decomposition
        for y in range(0, height, self.base_cell_size):
            for x in range(0, width, self.base_cell_size):
                cell = data[y:y+self.base_cell_size, x:x+self.base_cell_size]

                if cell.size == 0:
                    continue

                if self.contains_obstacle(cell):
                    # Step 2: adaptive subdivision
                    self.subdivide(
                        x, y,
                        self.base_cell_size,
                        data,
                        marker_array,
                        marker_id,
                        resolution
                    )
                else:
                    marker_array.markers.append(
                        self.create_marker(
                            x, y,
                            self.base_cell_size,
                            resolution,
                            marker_id,
                            free=True
                        )
                    )
                    marker_id += 1

        self.marker_pub.publish(marker_array)

    def contains_obstacle(self, cell):
        return np.any(cell > 50)

    def subdivide(self, x, y, size, data, marker_array, marker_id, resolution):
        if size <= self.min_cell_size:
            marker_array.markers.append(
                self.create_marker(
                    x, y, size, resolution, marker_id, free=False
                )
            )
            return

        half = size // 2
        for dy in [0, half]:
            for dx in [0, half]:
                sub = data[y+dy:y+dy+half, x+dx:x+dx+half]
                if sub.size == 0:
                    continue

                if self.contains_obstacle(sub):
                    self.subdivide(
                        x+dx, y+dy,
                        half,
                        data,
                        marker_array,
                        marker_id,
                        resolution
                    )
                else:
                    marker_array.markers.append(
                        self.create_marker(
                            x+dx, y+dy,
                            half,
                            resolution,
                            marker_id,
                            free=True
                        )
                    )
                    marker_id += 1

    def create_marker(self, x, y, size, resolution, marker_id, free=True):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "acd_cells"
        marker.id = marker_id
        marker.type = Marker.CUBE
        marker.action = Marker.ADD

        marker.scale.x = size * resolution
        marker.scale.y = size * resolution
        marker.scale.z = 0.01

        marker.pose.position.x = (x + size / 2) * resolution
        marker.pose.position.y = (y + size / 2) * resolution
        marker.pose.position.z = 0.0

        if free:
            marker.color.r = 0.0
            marker.color.g = 1.0
            marker.color.b = 0.0
            marker.color.a = 0.4
        else:
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 0.6

        return marker


def main(args=None):
    rclpy.init(args=args)
    node = AdaptiveCellDecomposition()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

