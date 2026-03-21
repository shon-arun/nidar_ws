#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from px4_msgs.msg import TrajectorySetpoint

class TargetSubscriber(Node):
    def __init__(self):
        super().__init__('target_node')
        # Create the subscriber for /target_altitude
        self.subscription = self.create_subscription(
            Float32,
            '/target_altitude',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.trajectory_pub = self.create_publisher(TrajectorySetpoint, '/fmu/in/trajectory_setpoint', 10)

        self.get_logger().info('Target Commander Active. Waiting for altitude commands...')

    def listener_callback(self, msg):
        target_alt = msg.data
        self.get_logger().info(f'Executing command: Ascending to {target_alt} meters')
        # self.get_logger().info(f'Received Target Altitude: {msg.data} m')

        # Create the PX4 physical command
        setpoint_msg = TrajectorySetpoint()

        # Conversion to the NED coordinate system
        setpoint_msg.position = [0.0, 0.0, -target_alt]
        setpoint_msg.yaw = 0.0 # Keep the drone facing North
        setpoint_msg.timestamp = int(self.get_clock().now().nanoseconds / 1000)

        self.trajectory_pub.publish(setpoint_msg)

def main(args=None):
    rclpy.init(args=args)
    node = TargetSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()