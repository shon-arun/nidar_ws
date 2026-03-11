import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='opsg_core',
            executable='altitude_node',
            name='altitude_publisher_node',
            output='screen'
        ),
        Node(
            package='opsg_core',
            executable='target_node',
            name='target_subscriber_node',
            output='screen'
        )
    ])