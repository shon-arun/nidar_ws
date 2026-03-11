#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class AltitudePublisher(Node):
    def __init__(self):
        super().__init__('altitude_node')
        # Create the publisher for /drone_altitude
        self.publisher_ = self.create_publisher(Float32, '/drone_altitude', 10)
        
        # Publish exactly twice a second (0.5 seconds)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.current_altitude = 0.0

    def timer_callback(self):
        msg = Float32()
        msg.data = self.current_altitude
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing Drone Altitude: {msg.data} m')
        
        # Simulate the drone slowly ascending
        self.current_altitude += 0.5

def main(args=None):
    rclpy.init(args=args)
    node = AltitudePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()