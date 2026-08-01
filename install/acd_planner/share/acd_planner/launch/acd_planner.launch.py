from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='acd_planner',
            executable='acd_planner',
            name='acd_planner_node',
            output='screen'
        )

    ])

