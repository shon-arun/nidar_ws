#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleOdometry
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
import math

class WaypointNode(Node):
    def __init__(self):
        super().__init__('waypoint_node')

        # 1. The Telemetry Reader (Using our battle-tested QoS profile)
        px4_qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        self.odom_sub = self.create_subscription(
            VehicleOdometry, '/fmu/out/vehicle_odometry', self.odom_callback, px4_qos_profile)

        # 2. The Flight Commanders
        self.trajectory_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', 10)
        self.offboard_mode_pub = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', 10)

        # 3. The Mission Array (North, East, Down)
        self.waypoints = [
            [0.0, 0.0, -5.0],   # WP 0: Takeoff to 5m
            [5.0, 0.0, -5.0],   # WP 1: Fly 5m North
            [5.0, 5.0, -5.0],   # WP 2: Fly 5m East
            [0.0, 5.0, -5.0],   # WP 3: Fly 5m South
            [0.0, 0.0, -5.0]    # WP 4: Fly 5m West (Return to start)
        ]
        
        self.current_wp_index = 0
        self.current_pos = [0.0, 0.0, 0.0]
        self.reached_threshold = 1.0  # Generous 1-meter radius to account for CoG wobble
        self.mission_complete = False

        # 10Hz Heartbeat Timer
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('Waypoint Navigator Active. Awaiting Offboard Mode...')

    def odom_callback(self, msg):
        # Constantly update our live 3D position
        self.current_pos = [msg.position[0], msg.position[1], msg.position[2]]

    def timer_callback(self):
        # 1. Satisfy the Dead Man's Switch
        mode_msg = OffboardControlMode()
        mode_msg.position = True
        mode_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.offboard_mode_pub.publish(mode_msg)

        # 2. Get current target
        target = self.waypoints[self.current_wp_index]

        # 3. Publish the Setpoint
        setpoint_msg = TrajectorySetpoint()
        setpoint_msg.position = target
        setpoint_msg.yaw = 0.0  # Keep the nose pointing North to watch it slide laterally
        setpoint_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)
        self.trajectory_pub.publish(setpoint_msg)

        # 4. Check the distance to the target using the Pythagorean theorem in 3D
        dx = self.current_pos[0] - target[0]
        dy = self.current_pos[1] - target[1]
        dz = self.current_pos[2] - target[2]
        distance = math.sqrt(dx**2 + dy**2 + dz**2)

        # 5. Advance the State Machine
        if distance < self.reached_threshold and not self.mission_complete:
            if self.current_wp_index < len(self.waypoints) - 1:
                self.current_wp_index += 1
                self.get_logger().info(f"Target Reached. Proceeding to WP {self.current_wp_index}: {self.waypoints[self.current_wp_index]}")
            else:
                self.mission_complete = True
                self.get_logger().info("Square Mission Complete! Hovering at origin.")

def main(args=None):
    rclpy.init(args=args)
    node = WaypointNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()